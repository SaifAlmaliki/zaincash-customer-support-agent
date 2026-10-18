from concurrent.futures import ThreadPoolExecutor
from threading import Barrier
from uuid import UUID, uuid4

from app.intake.contracts import Credentials


def _payload(view):
    return {
        "request_id": str(uuid4()), "expected_revision": view["revision"],
        "review_id": view["review"]["id"], "confirmed": True,
    }


def test_unsubmitted_session_is_hidden_from_employees(intake_client, reviewed):
    assert intake_client.get("/api/results").json()["items"] == []


def test_submission_replay_creates_one_ticket(intake_client, reviewed):
    url = f"/api/intake/sessions/{reviewed['sid']}/submit"
    payload = _payload(reviewed["view"])
    first = intake_client.post(url, headers=reviewed["headers"], json=payload)
    replay = intake_client.post(url, headers=reviewed["headers"], json=payload)
    assert first.status_code == replay.status_code == 200, first.text
    assert replay.json() == first.json()
    rows = intake_client.get("/api/results").json()["items"]
    assert len(rows) == 1
    assert rows[0]["status"] == "processing"
    assert rows[0]["ticket"]["external_id"] == first.json()["ticket_reference"]
    run = intake_client.get(f"/api/runs/{rows[0]['run_id']}").json()
    assert run["processed"] == 0 and run["total"] == 1


def test_second_request_id_reuses_the_approved_review(intake_client, reviewed):
    url = f"/api/intake/sessions/{reviewed['sid']}/submit"
    first = intake_client.post(url, headers=reviewed["headers"], json=_payload(reviewed["view"]))
    second = intake_client.post(url, headers=reviewed["headers"], json=_payload(reviewed["view"]))
    assert first.status_code == second.status_code == 200
    assert first.json()["ticket_reference"] == second.json()["ticket_reference"]
    changed = dict(_payload(reviewed["view"]), review_id=str(uuid4()))
    assert intake_client.post(url, headers=reviewed["headers"], json=changed).status_code == 409


def test_concurrent_submit_dispatches_once(intake_client, reviewed):
    service = intake_client.app.state.submission
    token = reviewed["headers"]["Authorization"].split()[1]
    credentials = Credentials(session_id=UUID(reviewed["sid"]), token=token)
    view = reviewed["view"]
    request_id = uuid4()
    barrier = Barrier(2)

    def once():
        barrier.wait()
        return service.submit(credentials, request_id, view["revision"], UUID(view["review"]["id"]), True)

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: once(), range(2)))
    assert sum(item.dispatch for item in results) == 1
    assert results[0].receipt.ticket_reference == results[1].receipt.ticket_reference
    assert len(intake_client.get("/api/results").json()["items"]) == 1
