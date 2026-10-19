from uuid import UUID, uuid4

from langchain_core.messages import AIMessage

from app.intake.contracts import Analysis, EvidenceRef, Fact
from app.intake.errors import ModelUnavailable
from app.intake.model import OpenRouterIntakeModel
from tests.intake.helpers import fact
from tests.intake.test_attachments import png_bytes


def test_review_after_failed_analysis_still_interprets_the_saved_message(intake_client):
    created = intake_client.post("/api/intake/sessions", json={"language": "en"}).json()
    sid = created["session"]["id"]
    headers = {"Authorization": f"Bearer {created['credentials']['token']}"}
    intake_client.model.analyses = [ModelUnavailable()]
    failed = intake_client.post(f"/api/intake/sessions/{sid}/messages", headers=headers, json={
        "request_id": str(uuid4()), "expected_revision": 0, "text": "What is the transfer fee?", "language": "en", "attachment_ids": [],
    }).json()
    reviewed = intake_client.post(f"/api/intake/sessions/{sid}/review", headers=headers, json={
        "request_id": str(uuid4()), "expected_revision": failed["revision"], "allow_partial": True, "language": "en",
    })
    assert reviewed.status_code == 200
    assert reviewed.json()["review"]["facts"]["issue"]["value"] == "What is the transfer fee?"


def test_validation_failure_retains_usage_audit(intake_client):
    class Ungrounded:
        async def ainvoke(self, messages):
            return {"raw": AIMessage(content="bad", response_metadata={"cost": 0.012}), "parsed": Analysis(
                language="en", category="general_inquiry", updates=[Fact(key="issue", status="known", value="invented",
                    evidence=[EvidenceRef(kind="message", source_id=uuid4(), quote="invented")])],
            )}

    app = intake_client.app
    app.state.intake.graph.model = OpenRouterIntakeModel(app.state.settings, runnable_factory=lambda schema: Ungrounded())
    owner, view = app.state.intake.repo.create("en")
    response = intake_client.post(f"/api/intake/sessions/{owner.session_id}/messages", headers={"Authorization": f"Bearer {owner.token}"}, json={
        "request_id": str(uuid4()), "expected_revision": view.revision, "text": "Help", "language": "en", "attachment_ids": [],
    }).json()
    assert response["turn_status"] == "retryable_failure"
    from sqlalchemy import select

    from app.intake.db_models import IntakeOperationRow
    with intake_client.factory() as session:
        operation = session.scalar(select(IntakeOperationRow).where(IntakeOperationRow.session_id == owner.session_id))
        assert len(operation.usage) == 2
        assert sum(item["cost_usd"] for item in operation.usage) == 0.024


def test_reinspection_keeps_current_images_and_new_observations(intake_client):
    service = intake_client.app.state.intake
    owner, view = service.repo.create("en")
    old_image, view = service.store.upload(owner, uuid4(), view.revision, "old.png", png_bytes())
    # A successful first turn records one source; the next explicitly reinspects it.
    headers = {"Authorization": f"Bearer {owner.token}"}
    first = intake_client.post(f"/api/intake/sessions/{owner.session_id}/messages", headers=headers, json={
        "request_id": str(uuid4()), "expected_revision": view.revision, "text": "What is the fee?", "language": "en", "attachment_ids": [str(old_image.id)],
    }).json()
    new_image, view = service.store.upload(owner, uuid4(), first["revision"], "new.png", png_bytes(color="black"))
    def initial(ctx):
        source = ctx.messages[-1]
        return Analysis(language="en", category="general_inquiry", updates=[fact("exact_error", "E-12", source)], reinspect_images=[old_image.id])
    def again(ctx):
        return Analysis(language="en", category="general_inquiry", updates=[Fact(key="txn_ref", status="known", value="DEMO-123", evidence=[
            EvidenceRef(kind="image", source_id=old_image.id, quote="DEMO-123"),
        ])])
    intake_client.model.analyses = [initial, again]
    second = intake_client.post(f"/api/intake/sessions/{owner.session_id}/messages", headers=headers, json={
        "request_id": str(uuid4()), "expected_revision": view.revision, "text": "E-12, compare receipts", "language": "en", "attachment_ids": [str(new_image.id)],
    }).json()
    assert second["review"]["facts"]["exact_error"]["value"] == "E-12"
    calls = [call for call in intake_client.model.calls if call[0] == "analyze"]
    assert set(calls[-1][2]) == {old_image.id, new_image.id}
    assert UUID(second["review"]["facts"]["txn_ref"]["evidence"][0]["source_id"]) == old_image.id
