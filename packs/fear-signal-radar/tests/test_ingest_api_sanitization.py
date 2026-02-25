from __future__ import annotations

import psycopg


def test_html_is_stripped_from_text_fields(client, auth_headers, signal_payload, admin_conn):
    payload = dict(signal_payload)
    payload["title"] = "<b>Hello</b><script>alert(1)</script> world"
    payload["text_snippet"] = "<div>Line <i>one</i></div><style>bad</style>"

    response = client.post("/ingest/signal", json=payload, headers=auth_headers)
    assert response.status_code == 201
    row_id = response.json()["id"]

    row = admin_conn.execute(
        "SELECT title, text_snippet FROM signal_items WHERE id = %s",
        (row_id,),
    ).fetchone()
    assert row[0] == "Hello world"
    assert row[1] == "Line one"


def test_length_caps_applied(client, auth_headers, signal_payload, admin_conn):
    payload = dict(signal_payload)
    payload["source_id"] = "cap-case-1"
    payload["title"] = "t" * 500
    payload["text_snippet"] = "s" * 3000
    payload["author"] = "a" * 500
    payload["url"] = "https://example.com/" + ("u" * 3000)

    response = client.post("/ingest/signal", json=payload, headers=auth_headers)
    assert response.status_code == 201
    row_id = response.json()["id"]

    row = admin_conn.execute(
        "SELECT title, text_snippet, author, url FROM signal_items WHERE id = %s",
        (row_id,),
    ).fetchone()

    assert len(row[0]) == 300
    assert len(row[1]) == 2000
    assert len(row[2]) == 100
    assert len(row[3]) == 2000


def test_max_body_size_rejected(client, auth_headers):
    large_payload = "x" * (300 * 1024)
    response = client.post(
        "/ingest/signal",
        content=large_payload,
        headers={**auth_headers, "Content-Type": "application/json"},
    )
    assert response.status_code == 413
