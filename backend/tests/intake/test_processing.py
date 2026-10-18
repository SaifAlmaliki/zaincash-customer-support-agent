from uuid import uuid4


def _submit(intake_client, reviewed):
    view = reviewed["view"]
    response = intake_client.post(f"/api/intake/sessions/{reviewed['sid']}/submit", headers=reviewed["headers"], json={
        "request_id": str(uuid4()), "expected_revision": view["revision"],
        "review_id": view["review"]["id"], "confirmed": True,
    })
    assert response.status_code == 200, response.text
    return response


def test_processing_ticket_rejects_review(intake_client, reviewed):
    _submit(intake_client, reviewed)
    row = intake_client.get("/api/results").json()["items"][0]
    response = intake_client.post(f"/api/results/{row['id']}/reviews", json={
        "action": "approve", "reviewer": "Agent", "final_text": "رد",
        "expected_updated_at": row["updated_at"],
    })
    assert response.status_code == 409


def test_committed_but_unscheduled_ticket_survives_recovery(intake_client, reviewed):
    from app.services.intake_recovery import recover_intake_processing
    _submit(intake_client, reviewed)
    assert recover_intake_processing(intake_client.app.state.session_factory) == 1
    row = intake_client.get("/api/results").json()["items"][0]
    assert row["status"] == "failed"
    detail = intake_client.get(f"/api/results/{row['id']}").json()
    assert detail["intake"]["messages"]
    assert recover_intake_processing(intake_client.app.state.session_factory) == 0
