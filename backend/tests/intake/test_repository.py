from datetime import UTC, datetime
from uuid import uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from app.config import Settings
from app.db.models import TicketRow
from app.db.session import init_db
from app.intake.contracts import Fact, Message
from app.intake.db_models import IntakeMessageRow, IntakeSessionRow


@pytest.fixture
def repo(intake_db):
    from app.intake.repository import IntakeRepository
    return IntakeRepository(intake_db[1])


def test_only_token_owner_can_resume(repo):
    from app.intake.contracts import Credentials
    from app.intake.errors import NotOwned
    owner, original = repo.create("ar")
    stranger, _ = repo.create("en")
    assert repo.get(owner).id == original.id
    with pytest.raises(NotOwned):
        repo.get(Credentials(session_id=owner.session_id, token=stranger.token))


def test_changed_payload_cannot_reuse_operation_identity():
    from app.intake.errors import OperationConflict
    from app.intake.repository import assert_same_operation, operation_fingerprint
    old = operation_fingerprint("message", {"text": "50000", "expected_revision": 1})
    same = operation_fingerprint("message", {"text": "50000", "expected_revision": 2})
    changed = operation_fingerprint("message", {"text": "5000", "expected_revision": 1})
    assert_same_operation(old, same)
    with pytest.raises(OperationConflict):
        assert_same_operation(old, changed)


def test_token_is_hashed_and_absent_from_the_view(repo, intake_db):
    import hashlib
    credentials, view = repo.create("ar")
    assert "token" not in view.model_dump(mode="json")
    with intake_db[1]() as session:
        row = session.get(IntakeSessionRow, credentials.session_id)
        assert row.token_hash == hashlib.sha256(credentials.token.encode("utf-8")).hexdigest()
        assert credentials.token not in row.token_hash
        assert row.review is None


def test_messages_keep_sequence_and_unicode(repo, intake_db):
    credentials, _ = repo.create("ar")
    now = datetime.now(UTC)
    with intake_db[1]() as session:
        session.add(IntakeMessageRow(
            id=uuid4(), session_id=credentials.session_id, sequence=2, role="assistant",
            text="ثاني", language="ar", created_at=now,
        ))
        session.add(IntakeMessageRow(
            id=uuid4(), session_id=credentials.session_id, sequence=1, role="user",
            text="أول ٥٠ ألف", language="ar", created_at=now,
        ))
        session.commit()
    view = repo.get(credentials)
    assert [item.text for item in view.messages] == ["أول ٥٠ ألف", "ثاني"]
    assert view.messages[0].created_at.tzinfo is not None


def test_datetimes_must_be_timezone_aware():
    with pytest.raises(ValidationError):
        Message(id=uuid4(), role="user", text="hello", language="en", created_at=datetime(2026, 10, 18))


def test_contracts_reject_extra_keys():
    with pytest.raises(ValidationError):
        Fact(key="issue", status="known", value="x", evidence=[], surprise="no")


def test_message_sequence_is_unique(repo, intake_db):
    credentials, _ = repo.create("en")
    now = datetime.now(UTC)
    with pytest.raises(IntegrityError):
        with intake_db[1]() as session:
            for _ in range(2):
                session.add(IntakeMessageRow(
                    id=uuid4(), session_id=credentials.session_id, sequence=1, role="user",
                    text="same", language="en", created_at=now,
                ))
            session.commit()


def test_repeated_init_db_keeps_existing_tickets(intake_db):
    settings, factory = intake_db
    with factory() as session:
        session.add(TicketRow(
            external_id="keep-me", channel="app", text="موجود", received_at=datetime.now(UTC), source="upload",
        ))
        session.commit()
    init_db(factory.kw["bind"])
    with factory() as session:
        assert session.query(TicketRow).filter_by(external_id="keep-me").one().text == "موجود"


def test_blank_intake_model_is_rejected():
    with pytest.raises(ValidationError):
        Settings(_env_file=None, intake_model="  ")
    assert Settings(_env_file=None, intake_model="").intake_model == ""


def test_non_positive_image_limit_is_rejected():
    with pytest.raises(ValidationError):
        Settings(_env_file=None, intake_max_image_bytes=0)
