from __future__ import annotations


def test_missing_authorization_header_returns_401(client, signal_payload):
    response = client.post("/ingest/signal", json=signal_payload)
    assert response.status_code == 401


def test_wrong_token_returns_401(client, signal_payload):
    response = client.post(
        "/ingest/signal",
        json=signal_payload,
        headers={"Authorization": "Bearer wrong-token"},
    )
    assert response.status_code == 401


def test_correct_token_allows_request(client, auth_headers, signal_payload):
    response = client.post("/ingest/signal", json=signal_payload, headers=auth_headers)
    assert response.status_code == 201
    assert response.json()["status"] == "created"
