"""Atomic claim/compute/publish indexing and compatible pgvector retrieval."""
from __future__ import annotations

import asyncio
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from hashlib import sha256
from math import ceil
from threading import Event, Lock
from time import monotonic
from uuid import uuid4

from sqlalchemy import delete, event, or_, select
from sqlalchemy.orm import Session, sessionmaker

from app.config import Settings
from app.db.document_models import UploadedDocument
from app.kb.contracts import Embedder, EmbeddingBatch, Passage, SearchResult, TextChunk
from app.kb.documents import document_view
from app.kb.models import KnowledgeChunk, KnowledgeDocumentIndex
from app.kb.parse import DocumentParseError, parse_document
from app.taxonomy import load_taxonomy

INDEXING_TIMEOUT_S = 120
CHUNKING_VERSION = "unicode-1200-overlap-180-v1"


class KnowledgeError(RuntimeError):
    """Public service error; cost is this invocation's measured embedding cost."""

    def __init__(self, message: str, *, cost_usd: float = 0.0) -> None:
        super().__init__(message)
        self.cost_usd = cost_usd


class KnowledgeExecutionError(RuntimeError):
    """Unexpected retrieval fault: safe diagnostic identity and measured cost only."""

    def __init__(self, cause: Exception, *, cost_usd: float = 0.0) -> None:
        self.diagnostic_type = type(cause).__name__
        super().__init__(f"{self.diagnostic_type}: unexpected knowledge retrieval fault.")
        self.cost_usd = cost_usd


class DocumentNotFoundError(KnowledgeError, LookupError):
    pass


class IndexAttemptLostError(KnowledgeError):
    pass


@dataclass(frozen=True)
class _Claim:
    document_id: int
    filename: str
    digest: str
    content: bytes
    attempt_id: str
    model: str
    dimensions: int
    tags: tuple[str, ...]


def _error_cost(error: BaseException) -> float:
    # TimeoutError carries the adapter's cancellation as its cause. These are
    # alternative outcomes of one call, never sums of the same provider response.
    if hasattr(error, "cost_usd"):
        return error.cost_usd
    if isinstance(error, TimeoutError) and error.__cause__ is not None:
        return getattr(error.__cause__, "cost_usd", 0.0)
    return 0.0


def _check_deadline(deadline: float) -> None:
    if monotonic() >= deadline:
        raise TimeoutError


def _abandoned(error: BaseException) -> bool:
    return getattr(error, "_kb_db_abandoned", False) or getattr(
        error.__cause__, "_kb_db_abandoned", False,
    )


def _consume(future) -> None:
    if not future.cancelled():
        future.exception()


class _DatabaseCall:
    """One worker's cancellation fence, never configuration on the shared engine."""

    def __init__(self, deadline: float, on_abandon=None):
        self.deadline = deadline
        self.stopped = Event()
        self._finished = False
        self._cancel_requested = False
        self._commit_owned = False
        self._finish_lock = Lock()
        self._connection_lock = Lock()
        self._connection = None
        self._on_abandon = on_abandon

    def check(self) -> None:
        if self.stopped.is_set():
            raise TimeoutError("Database operation was cancelled.")
        _check_deadline(self.deadline)

    def attach(self, connection) -> None:
        with self._finish_lock:
            self._commit_owned = False
            if self._cancel_requested:
                self.stopped.set()
        with self._connection_lock:
            self._connection = connection
        self.check()

    def detach(self) -> None:
        # Synchronize with cancellation before returning the connection to its pool:
        # a late cancel request must never hit another borrower's query.
        with self._connection_lock:
            self._connection = None

    def cancel_query(self) -> None:
        with self._connection_lock:
            if self._connection is not None:
                try:
                    self._connection.cancel_safe(timeout=1.0)
                except Exception:
                    # SQL deadlines and the commit fence remain authoritative even
                    # if a driver/server cannot acknowledge query cancellation.
                    pass

    def _set_timeout(self, cursor) -> None:
        self.check()
        milliseconds = max(1, ceil((self.deadline - monotonic()) * 1000))
        cursor.execute("SELECT set_config('statement_timeout', %s, true)", (f"{milliseconds}ms",))
        self.check()

    def before_execute(self, connection, *_args) -> None:
        # Run before SQLAlchemy cursor hooks too, so time spent in those hooks is
        # charged to this statement rather than escaping its remaining budget.
        with connection.connection.driver_connection.cursor() as cursor:
            self._set_timeout(cursor)

    def before_cursor(self, _connection, cursor, *_args) -> None:
        # Recompute for every execution, including ORM flush / insertmanyvalues.
        self._set_timeout(cursor)

    def after_cursor(self, *_args) -> None:
        self.check()

    def before_commit(self, connection) -> None:
        self.before_execute(connection)

    def commit(self, dbapi_commit) -> None:
        # Linearization point: the DBAPI handoff and abandonment compete under
        # one short lock. Once handed off, COMMIT owns its outcome; cancellation
        # can detach the caller but must not stop/cancel this transaction. The
        # lock is never held during driver I/O or acquired there by the loop.
        with self._finish_lock:
            self.check()
            self._commit_owned = True
        try:
            dbapi_commit()
        except BaseException:
            with self._finish_lock:
                self._commit_owned = False
                if self._cancel_requested:
                    self.stopped.set()
            raise

    def cleanup(self) -> None:
        if self._on_abandon is not None:
            try:
                self._on_abandon()
            except Exception:
                # The caller already has the measured cost; startup recovery is
                # the fallback when the database cannot record failure.
                pass

    def run(self, function):
        try:
            self.check()
            result = function(self)
            self.check()
            return result
        finally:
            with self._finish_lock:
                self._finished = True
                cleanup = self._cancel_requested
            if cleanup:
                self.cleanup()

    def abandon(self, loop) -> None:
        with self._finish_lock:
            if self._cancel_requested:
                return
            self._cancel_requested = True
            if not self._commit_owned:
                self.stopped.set()
            cancel_query = self.stopped.is_set()
            finished = self._finished
        if cancel_query:
            loop.run_in_executor(None, self.cancel_query).add_done_callback(_consume)
        # If the worker finished just before cancellation was delivered, it could
        # not see the stop flag in its finally block. Exactly one side cleans up.
        if finished:
            loop.run_in_executor(None, self.cleanup).add_done_callback(_consume)


class KnowledgeService:
    def __init__(self, session_factory: sessionmaker, settings: Settings, embedder: Embedder):
        self._sessions = session_factory
        self._settings = settings
        self._embedder = embedder
        self._categories = frozenset(load_taxonomy(settings.taxonomy_path).ids)
        self._metadata()

    async def _database(self, deadline: float, function, *, on_abandon=None):
        call = _DatabaseCall(deadline, on_abandon)
        loop = asyncio.get_running_loop()
        future = loop.run_in_executor(None, call.run, function)
        future.add_done_callback(_consume)
        try:
            return await asyncio.wait_for(asyncio.shield(future), max(0, deadline - monotonic()))
        except (asyncio.CancelledError, TimeoutError) as exc:
            call.abandon(loop)
            exc._kb_db_abandoned = True
            raise

    @contextmanager
    def _transaction(self, call: _DatabaseCall):
        # Checkout, SQL, flush, commit and rollback all execute in the worker.
        # A cancelled checkout cannot be killed, but its eventual connection is
        # fenced before any SQL and returned to the pool by this context manager.
        with self._sessions() as session, session.get_bind().connect() as connection:
            session.bind = connection
            driver = connection.connection.driver_connection
            original_commit = driver.commit
            had_commit_override = "commit" in vars(driver)
            listeners = (
                ("before_execute", call.before_execute),
                ("before_cursor_execute", call.before_cursor),
                ("after_cursor_execute", call.after_cursor),
                ("commit", call.before_commit),
            )
            try:
                call.attach(driver)
                # Borrower-local interception at the actual DBAPI boundary, not
                # a SQLAlchemy event which still precedes an unchecked commit.
                driver.commit = lambda: call.commit(original_commit)
                for name, listener in listeners:
                    event.listen(connection, name, listener)
                with session.begin():
                    yield session
                    session.flush()
                    call.check()
            finally:
                session.close()
                if had_commit_override:
                    driver.commit = original_commit
                elif "commit" in vars(driver):
                    del driver.commit
                call.detach()
                for name, listener in listeners:
                    if event.contains(connection, name, listener):
                        event.remove(connection, name, listener)

    def _metadata(self) -> tuple[str, int]:
        if (self._embedder.model != self._settings.embedding_model
                or self._embedder.dimensions != self._settings.embed_dim
                or self._embedder.dimensions != 768):
            raise ValueError("Embedding configuration does not match the provider/index schema.")
        return self._embedder.model, self._embedder.dimensions

    def _tags(self, tags: list[str]) -> list[str]:
        if any(tag not in self._categories for tag in tags):
            raise ValueError("Unknown knowledge category; use a taxonomy category ID.")
        return sorted(set(tags))

    @staticmethod
    def _source(session: Session, document_id: int, *, cost: float = 0.0) -> UploadedDocument:
        document = session.scalar(select(UploadedDocument).where(
            UploadedDocument.id == document_id).with_for_update())
        if document is None:
            raise DocumentNotFoundError("Document not found.", cost_usd=cost)
        return document

    def _claim(
        self, document_id: int, tags: list[str] | None, attempt_id: str, call: _DatabaseCall,
    ) -> _Claim | dict:
        model, dimensions = self._metadata()
        with self._transaction(call) as session:
            # The source exists before the index row does: it is the shared lock
            # for first claims, retries, publication, recovery and deletion.
            document = self._source(session, document_id)
            index = session.get(KnowledgeDocumentIndex, document_id, with_for_update=True)
            if index is not None and index.status == "indexing":
                return document_view(session, document)
            if index is None:
                index = KnowledgeDocumentIndex(document_id=document_id)
                session.add(index)
            selected_tags = tags if tags is not None else (index.category_tags or [])
            index.status = "indexing"
            index.attempt_id = attempt_id
            index.embedding_model = model
            index.embedding_dimensions = dimensions
            index.chunking_version = CHUNKING_VERSION
            index.category_tags = list(selected_tags)
            index.error = None
            index.updated_at = datetime.now(UTC)
            session.flush()
            return _Claim(document_id, document.filename, document.sha256, document.content,
                          attempt_id, model, dimensions, tuple(selected_tags))

    def _owned(self, session: Session, claim: _Claim, cost: float):
        document = self._source(session, claim.document_id, cost=cost)
        index = session.get(KnowledgeDocumentIndex, claim.document_id, with_for_update=True)
        if (index is None or index.status != "indexing" or index.attempt_id != claim.attempt_id
                or document.sha256 != claim.digest or index.embedding_model != claim.model
                or index.embedding_dimensions != claim.dimensions):
            raise IndexAttemptLostError("Indexing attempt was superseded; its result was discarded.",
                                        cost_usd=cost)
        return document, index

    def _publish(
        self, claim: _Claim, chunks: list[TextChunk], batch: EmbeddingBatch, call: _DatabaseCall,
    ) -> dict:
        with self._transaction(call) as session:
            document, index = self._owned(session, claim, batch.cost_usd)
            session.execute(delete(KnowledgeChunk).where(KnowledgeChunk.document_id == claim.document_id))
            for chunk, vector in zip(chunks, batch.vectors, strict=True):
                identity = f"{claim.digest}\0{CHUNKING_VERSION}\0{chunk.index}\0{chunk.text}"
                session.add(KnowledgeChunk(
                    id=sha256(identity.encode("utf-8")).hexdigest(), document_id=claim.document_id,
                    attempt_id=claim.attempt_id, chunk_index=chunk.index, text=chunk.text,
                    filename=claim.filename, page_start=chunk.page_start, page_end=chunk.page_end,
                    category_tags=list(claim.tags), embedding_model=claim.model, embedding=list(vector),
                ))
            index.status = "indexed"
            index.chunk_count = len(chunks)
            index.cost_usd += batch.cost_usd
            index.error = None
            index.indexed_at = index.updated_at = datetime.now(UTC)
            session.flush()
            return document_view(session, document)

    def _fail(
        self, document_id: int, attempt_id: str, message: str, cost: float, call: _DatabaseCall,
    ) -> dict:
        try:
            with self._transaction(call) as session:
                document = self._source(session, document_id, cost=cost)
                index = session.get(KnowledgeDocumentIndex, document_id, with_for_update=True)
                if index is None or index.status != "indexing" or index.attempt_id != attempt_id:
                    raise IndexAttemptLostError("Indexing attempt was superseded; its result was discarded.",
                                                cost_usd=cost)
                index.status = "failed"
                index.error = message[:512]
                index.cost_usd += cost
                index.updated_at = datetime.now(UTC)
                session.flush()
                return document_view(session, document)
        except KnowledgeError:
            raise
        except Exception:
            raise KnowledgeError("Unable to record indexing failure; retry after database recovery.",
                                 cost_usd=cost) from None

    def _abandon_attempt(self, document_id: int, attempt_id: str, cost: float) -> None:
        call = _DatabaseCall(monotonic() + 1.0)
        # A cancelled first claim may never have acquired the source lock. Do not
        # wait for that same lock again just to discover there is no owned row.
        with self._transaction(call) as session:
            owned = session.scalar(select(KnowledgeDocumentIndex.document_id).where(
                KnowledgeDocumentIndex.document_id == document_id,
                KnowledgeDocumentIndex.attempt_id == attempt_id,
                KnowledgeDocumentIndex.status == "indexing",
            ))
        if owned is None:
            return
        self._fail(document_id, attempt_id, "Indexing database work was interrupted; retry indexing.",
                   cost, call)

    async def _record_failure(self, document_id: int, attempt_id: str, message: str, cost: float):
        try:
            return await self._database(
                monotonic() + 1.0,
                lambda call: self._fail(document_id, attempt_id, message, cost, call),
                on_abandon=lambda: self._abandon_attempt(document_id, attempt_id, cost),
            )
        except asyncio.CancelledError as exc:
            exc.cost_usd = cost
            raise
        except KnowledgeError:
            raise
        except Exception:
            raise KnowledgeError("Unable to record indexing failure; retry after database recovery.",
                                 cost_usd=cost) from None

    async def index_document(self, document_id: int, *, category_tags: list[str] | None = None) -> dict:
        """Reindex a source; an active claim returns its current projection without work.

        Failures return a retryable failed projection. Cancellation propagates after
        recording cost. Deleted/superseded completions raise cost-bearing errors.
        """
        tags = self._tags(category_tags) if category_tags is not None else None
        deadline = monotonic() + INDEXING_TIMEOUT_S
        attempt_id = str(uuid4())
        claim = None
        cost = 0.0
        embedded = False
        try:
            async with asyncio.timeout(INDEXING_TIMEOUT_S) as timeout:
                claim = await self._database(
                    deadline, lambda call: self._claim(document_id, tags, attempt_id, call),
                    on_abandon=lambda: self._abandon_attempt(document_id, attempt_id, 0.0),
                )
                if isinstance(claim, dict):
                    return claim
                # Parsing can be CPU-bound. No database session lives across either await.
                chunks = await asyncio.to_thread(parse_document, claim.filename, claim.content)
                batch = await self._embedder.embed([chunk.text for chunk in chunks])
                cost, embedded = batch.cost_usd, True
                # Also reject providers that suppress deadline cancellation and finish late.
                if timeout.expired():
                    raise TimeoutError
                _check_deadline(deadline)
                if self._metadata() != (claim.model, claim.dimensions):
                    raise ValueError("Embedding model changed during indexing.")
                return await self._database(
                    deadline, lambda call: self._publish(claim, chunks, batch, call),
                    on_abandon=lambda: self._abandon_attempt(document_id, attempt_id, cost),
                )
        except asyncio.CancelledError as exc:
            cost = cost if embedded else _error_cost(exc)
            exc.cost_usd = cost
            try:
                if claim is not None and not _abandoned(exc):
                    await self._record_failure(
                        document_id, attempt_id, "Indexing was cancelled; retry indexing.", cost,
                    )
            except KnowledgeError:
                # Cancellation must retain its identity, including when ownership is lost.
                pass
            raise
        except (DocumentNotFoundError, IndexAttemptLostError):
            raise
        except Exception as exc:
            cost = cost if embedded else _error_cost(exc)
            if _abandoned(exc):
                raise KnowledgeError("Indexing database work timed out; retry indexing.",
                                     cost_usd=cost) from None
            if claim is None:
                raise KnowledgeError("Unable to claim document for indexing; retry.",
                                     cost_usd=cost) from None
            if isinstance(exc, DocumentParseError):
                message = str(exc)
            elif isinstance(exc, TimeoutError):
                message = "Indexing timed out; retry with a smaller document."
            else:
                message = "Indexing failed; check embedding configuration and retry."
            return await self._record_failure(document_id, attempt_id, message, cost)

    async def search(self, query: str, *, category: str | None = None, k: int = 5) -> SearchResult:
        if category is not None:
            self._tags([category])
        if not query.strip():
            raise ValueError("Knowledge query must not be empty.")
        if type(k) is not int:
            raise ValueError("Knowledge search limit must be an integer.")
        limit = max(1, min(k, 10))
        model, dimensions = self._metadata()
        deadline = monotonic() + self._settings.agent_timeout_s
        # Leave adapter errors/cancellation intact for the owning drafting boundary.
        batch = await self._embedder.embed([query])
        try:
            if self._metadata() != (model, dimensions):
                raise ValueError("Embedding model changed during search.")
            vector, = batch.vectors
            distance = KnowledgeChunk.embedding.cosine_distance(list(vector))
            statement = select(KnowledgeChunk, distance.label("distance")).join(
                KnowledgeDocumentIndex, KnowledgeChunk.document_id == KnowledgeDocumentIndex.document_id,
            ).where(
                KnowledgeDocumentIndex.status == "indexed",
                KnowledgeDocumentIndex.embedding_model == model,
                KnowledgeDocumentIndex.embedding_dimensions == dimensions,
                KnowledgeDocumentIndex.chunking_version == CHUNKING_VERSION,
                KnowledgeChunk.embedding_model == model,
                KnowledgeChunk.attempt_id == KnowledgeDocumentIndex.attempt_id,
                distance <= 1 - self._settings.kb_min_similarity,
            )
            if category is not None:
                statement = statement.where(or_(
                    KnowledgeChunk.category_tags.contains([category]),
                    KnowledgeChunk.category_tags == [],
                ))
            statement = statement.order_by(distance, KnowledgeChunk.id).limit(limit)
            passages = await self._database(deadline, lambda call: self._read_passages(statement, call))
            return SearchResult(passages, batch.cost_usd)
        except asyncio.CancelledError as exc:
            exc.cost_usd = batch.cost_usd
            raise
        except TimeoutError:
            raise KnowledgeError("Knowledge retrieval timed out; retry after checking the index.",
                                  cost_usd=batch.cost_usd) from None
        except Exception as exc:
            raise KnowledgeExecutionError(exc, cost_usd=batch.cost_usd) from None

    def _read_passages(self, statement, call: _DatabaseCall) -> tuple[Passage, ...]:
        with self._transaction(call) as session:
            return tuple(Passage(
                id=chunk.id, document_id=chunk.document_id, chunk_index=chunk.chunk_index,
                text=chunk.text, filename=chunk.filename, score=1 - float(value),
                page_start=chunk.page_start, page_end=chunk.page_end,
            ) for chunk, value in session.execute(statement))

    def recover_interrupted(self) -> int:
        """Startup-only recovery for this single-worker app, before scheduling jobs."""
        with self._sessions() as session:
            abandoned = session.execute(select(
                KnowledgeDocumentIndex.document_id, KnowledgeDocumentIndex.attempt_id,
            ).where(KnowledgeDocumentIndex.status == "indexing")).all()
        recovered = 0
        for document_id, attempt_id in abandoned:
            with self._sessions.begin() as session:
                document = session.scalar(select(UploadedDocument).where(
                    UploadedDocument.id == document_id).with_for_update())
                if document is None:
                    continue
                index = session.get(KnowledgeDocumentIndex, document_id, with_for_update=True)
                if index is not None and index.status == "indexing" and index.attempt_id == attempt_id:
                    index.status = "failed"
                    index.attempt_id = None
                    index.error = "Indexing was interrupted by process restart; retry indexing."
                    index.updated_at = datetime.now(UTC)
                    recovered += 1
        return recovered

    def list_chunks(self, document_id: int) -> list[dict]:
        """Inspect retained published chunks in source order, including after a failed retry."""
        with self._sessions() as session:
            if session.get(UploadedDocument, document_id) is None:
                raise DocumentNotFoundError("Document not found.")
            chunks = session.scalars(select(KnowledgeChunk).where(
                KnowledgeChunk.document_id == document_id).order_by(KnowledgeChunk.chunk_index))
            return [{
                "id": chunk.id, "document_id": chunk.document_id, "chunk_index": chunk.chunk_index,
                "text": chunk.text, "filename": chunk.filename,
                "page_start": chunk.page_start, "page_end": chunk.page_end,
                "category_tags": list(chunk.category_tags), "embedding_model": chunk.embedding_model,
            } for chunk in chunks]
