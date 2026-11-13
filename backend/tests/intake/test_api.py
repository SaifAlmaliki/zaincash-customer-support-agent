from uuid import uuid4


def test_session_requires_a_valid_customer_phone(intake_client):
    assert intake_client.post("/api/intake/sessions", json={"language": "en"}).status_code == 422
    invalid = intake_client.post("/api/intake/sessions", json={"language": "en", "customer_phone": "12345"})
    assert invalid.status_code == 422
    assert invalid.json()["detail"]["code"] == "invalid_phone"
    created = intake_client.post("/api/intake/sessions", json={"language": "en", "customer_phone": "٠٧٧٠١٢٣٤٥٦٧"})
    assert created.status_code == 201
    assert created.json()["session"]["customer_phone"] == "07701234567"
    sid = created.json()["credentials"]["session_id"]
    headers = {"Authorization": f"Bearer {created.json()['credentials']['token']}"}
    assert intake_client.get(f"/api/intake/sessions/{sid}", headers=headers).json()["customer_phone"] == "07701234567"


def test_message_replay_is_single_turn(intake_client):
    created = intake_client.post("/api/intake/sessions", json={"language": "en", "customer_phone": "07701234567"}).json()
    sid, token = created["credentials"]["session_id"], created["credentials"]["token"]
    headers = {"Authorization": f"Bearer {token}"}
    url = f"/api/intake/sessions/{sid}/messages"
    body = {"request_id": str(uuid4()), "expected_revision": 0,
            "text": "My transfer failed", "language": "en", "attachment_ids": []}
    first = intake_client.post(url, headers=headers, json=body)
    second = intake_client.post(url, headers=headers, json=body)
    assert first.status_code == second.status_code == 200, first.text
    assert [item["id"] for item in first.json()["messages"]] == [item["id"] for item in second.json()["messages"]]
    changed = intake_client.post(url, headers=headers, json=body | {"text": "Different issue"})
    assert changed.status_code == 409


def test_missing_token_and_stale_revision(intake_client):
    created = intake_client.post("/api/intake/sessions", json={"language": "ar", "customer_phone": "07701234567"}).json()
    sid = created["credentials"]["session_id"]
    missing = intake_client.get(f"/api/intake/sessions/{sid}")
    assert missing.status_code == 401
    headers = {"Authorization": f"Bearer {created['credentials']['token']}"}
    stale = intake_client.post(f"/api/intake/sessions/{sid}/messages", headers=headers, json={
        "request_id": str(uuid4()), "expected_revision": 4, "text": "مرحبا", "language": "ar", "attachment_ids": [],
    })
    assert stale.status_code == 409


def test_resume_uses_a_new_service_state(intake_client):
    created = intake_client.post("/api/intake/sessions", json={"language": "en", "customer_phone": "07701234567"}).json()
    headers = {"Authorization": f"Bearer {created['credentials']['token']}"}
    sid = created["credentials"]["session_id"]
    sent = intake_client.post(f"/api/intake/sessions/{sid}/messages", headers=headers, json={
        "request_id": str(uuid4()), "expected_revision": 0, "text": "Fee question", "language": "en", "attachment_ids": [],
    })
    assert sent.status_code == 200, sent.text
    again = intake_client.get(f"/api/intake/sessions/{sid}", headers=headers)
    assert again.json()["revision"] == sent.json()["revision"]
    assert again.json()["messages"]
