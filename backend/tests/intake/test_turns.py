from uuid import uuid4

import pytest

from app.intake.contracts import TurnResult
from app.intake.errors import RevisionConflict


@pytest.fixture
def repo(intake_db):
    from app.intake.repository import IntakeRepository
    return IntakeRepository(intake_db[1])


@pytest.fixture
def turns(intake_db):
    from app.intake.turns import TurnStore
    return TurnStore(intake_db[1])


def test_recovered_attempt_cannot_publish_stale_output(repo, turns):
    owner, view = repo.create("en")
    request_id = uuid4()
    old = turns.claim(owner, "message", request_id, view.revision,
                      {"text": "Transfer failed", "language": "en", "attachment_ids": []})
    turns.recover_interrupted()
    fresh = turns.retry(owner, request_id, repo.get(owner).revision)
    with pytest.raises(RevisionConflict):
        turns.finish(old, TurnResult(old.context.state, "Stale question", None, []))
    saved = turns.finish(fresh, TurnResult(fresh.context.state, "Current question", None, []))
    assert "Stale question" not in [item.text for item in saved.messages]
    assert [item.text for item in saved.messages].count("Transfer failed") == 1


def test_review_publication_revision_matches_the_session(repo, turns):
    from app.intake.contracts import ReviewSnapshot
    from tests.intake.helpers import grounded_review
    owner, view = repo.create("en")
    claimed = turns.claim(owner, "message", uuid4(), view.revision, {
        "text": "What is the transfer fee?", "language": "en", "attachment_ids": [],
    })
    review = ReviewSnapshot(
        id=uuid4(), revision=claimed.revision + 1, language="en", quality="sufficient_context",
        facts=claimed.context.state.facts, additional_issues=[], unknown_keys=[],
        customer_text="Fee question", employee_text_ar="سؤال عن العمولة", ticket_text_ar="سؤال عن العمولة",
        attachment_ids=[],
    )
    saved = turns.finish(claimed, TurnResult(claimed.context.state, "Please review.", review, []))
    assert saved.review is not None
    assert saved.review.revision == saved.revision
    assert grounded_review
