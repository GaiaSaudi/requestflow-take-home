from fastapi.testclient import TestClient


def headers(token: str) -> dict[str, str]:
    return {"X-Session-Token": token}


def test_health_and_session_boundary(client: TestClient) -> None:
    assert client.get("/health").json() == {"status": "ok"}
    assert client.get("/api/session").status_code == 401
    response = client.get("/api/session", headers=headers("session-bob"))
    assert response.status_code == 200
    assert response.json()["name"] == "Bob"


def test_visible_request_can_be_read(client: TestClient) -> None:
    response = client.get("/api/requests/1", headers=headers("session-bob"))
    assert response.status_code == 200
    assert response.json()["status"] == "pending"


def test_starter_happy_path_records_history(client: TestClient) -> None:
    response = client.post(
        "/api/requests/1/decision",
        headers=headers("session-bob"),
        json={
            "actor_id": 2,
            "decision": "approved",
            "reason": "Starter happy path",
            "idempotency_key": "public-test-approval",
            "expected_version": 1,
        },
    )
    assert response.status_code == 200
    assert response.json()["request"]["status"] == "approved"

    history = client.get("/api/requests/1/history", headers=headers("session-bob")).json()
    assert len(history) == 1
    assert history[0]["decision"] == "approved"


def test_terminal_request_returns_conflict(client: TestClient) -> None:
    payload = {
        "actor_id": 2,
        "decision": "approved",
        "reason": None,
        "idempotency_key": "first-command",
        "expected_version": 1,
    }
    assert (
        client.post(
            "/api/requests/1/decision", headers=headers("session-bob"), json=payload
        ).status_code
        == 200
    )
    payload["idempotency_key"] = "second-command"
    assert (
        client.post(
            "/api/requests/1/decision", headers=headers("session-bob"), json=payload
        ).status_code
        == 409
    )
