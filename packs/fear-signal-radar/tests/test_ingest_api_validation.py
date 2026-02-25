from __future__ import annotations

import pytest


@pytest.mark.parametrize(
    "missing_key",
    ["topic_id", "platform", "content_type", "url"],
)
def test_missing_required_fields_returns_422(client, auth_headers, signal_payload, missing_key):
    payload = dict(signal_payload)
    payload.pop(missing_key)

    response = client.post("/ingest/signal", json=payload, headers=auth_headers)
    assert response.status_code == 422


def test_invalid_platform_enum_returns_422(client, auth_headers, signal_payload):
    payload = dict(signal_payload)
    payload["platform"] = "tiktok"

    response = client.post("/ingest/signal", json=payload, headers=auth_headers)
    assert response.status_code == 422


def test_additional_unexpected_field_rejected(client, auth_headers, signal_payload):
    payload = dict(signal_payload)
    payload["unexpected"] = "nope"

    response = client.post("/ingest/signal", json=payload, headers=auth_headers)
    assert response.status_code == 422
