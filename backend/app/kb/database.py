"""Borrower-local database deadlines, cancellation, and commit handoff."""
from math import ceil
from threading import Event, Lock
from time import monotonic


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
