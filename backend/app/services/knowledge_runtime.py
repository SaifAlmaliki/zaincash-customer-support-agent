"""Application wiring and bounded admission; KnowledgeService owns index state/cost."""
import logging
from threading import Lock

from app.kb.embeddings import OpenRouterEmbedder
from app.kb.service import KnowledgeService

logger = logging.getLogger(__name__)
MAX_INDEX_JOBS = 4


def make_knowledge_service(session_factory, settings):
    # The adapter owns a short-lived HTTP client per invocation, not per app.
    return KnowledgeService(session_factory, settings, OpenRouterEmbedder(settings))


def knowledge_configured(settings):
    return settings.rag_enabled and bool(settings.openrouter_api_key)


class IndexJobs:
    """Single-process admission, including the gap before BackgroundTasks starts.

    No queue or detached tasks: accepted work runs in the response background and
    the service enforces its 120s deadline using independent database sessions.
    """

    def __init__(self, service):
        self.service = service
        self._pending = set()
        self._lock = Lock()

    def submit(self, background, document, *, category_tags=None):
        document_id = document["id"]
        with self._lock:
            if document_id in self._pending or document["status"] == "indexing":
                return True
            if len(self._pending) >= MAX_INDEX_JOBS:
                return False
            self._pending.add(document_id)
        background.add_task(self.run, document_id, category_tags)
        return True

    async def run(self, document_id, category_tags):
        try:
            await self.service.index_document(document_id, category_tags=category_tags)
        except Exception as exc:
            # Normal failures are persisted by the service. Lost/deleted attempts
            # cannot be written back: report their cost once at this job boundary.
            logger.warning("Index job %s ended: %s; invocation cost_usd=%s",
                           document_id, type(exc).__name__, getattr(exc, "cost_usd", 0.0))
        finally:
            with self._lock:
                self._pending.discard(document_id)
