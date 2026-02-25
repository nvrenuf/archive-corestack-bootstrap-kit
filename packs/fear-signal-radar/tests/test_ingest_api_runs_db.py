from __future__ import annotations


def test_run_start_creates_row(client, auth_headers, admin_conn):
    payload = {"topic_id": "work-money", "time_window_days": 7}
    response = client.post("/ingest/run/start", json=payload, headers=auth_headers)

    assert response.status_code == 201
    run_id = response.json()["run_id"]

    row = admin_conn.execute(
        "SELECT run_id, status, started_at FROM radar_runs WHERE run_id = %s",
        (run_id,),
    ).fetchone()
    assert str(row[0]) == run_id
    assert row[1] == "ok"
    assert row[2] is not None


def test_run_finish_updates_status_and_counts(client, auth_headers, admin_conn):
    start_payload = {"topic_id": "work-money", "time_window_days": 7}
    start_response = client.post("/ingest/run/start", json=start_payload, headers=auth_headers)
    run_id = start_response.json()["run_id"]

    finish_payload = {
        "run_id": run_id,
        "status": "ok",
        "counts_json": {"collected": 5, "inserted": 4, "duplicates": 1},
    }
    finish_response = client.post("/ingest/run/finish", json=finish_payload, headers=auth_headers)

    assert finish_response.status_code == 200
    assert finish_response.json() == {"status": "updated", "run_id": run_id}

    row = admin_conn.execute(
        "SELECT status, counts_json, finished_at, error_text FROM radar_runs WHERE run_id = %s",
        (run_id,),
    ).fetchone()

    assert row[0] == "ok"
    assert row[1] == {"collected": 5, "inserted": 4, "duplicates": 1}
    assert row[2] is not None
    assert row[3] is None


def test_run_finish_error_persists_error_text(client, auth_headers, admin_conn):
    start_payload = {"topic_id": "work-money", "time_window_days": 7}
    start_response = client.post("/ingest/run/start", json=start_payload, headers=auth_headers)
    run_id = start_response.json()["run_id"]

    finish_payload = {
        "run_id": run_id,
        "status": "error",
        "counts_json": {"collected": 0, "inserted": 0, "duplicates": 0},
        "error_text": "collector timeout",
    }
    finish_response = client.post("/ingest/run/finish", json=finish_payload, headers=auth_headers)

    assert finish_response.status_code == 200

    row = admin_conn.execute(
        "SELECT status, error_text FROM radar_runs WHERE run_id = %s",
        (run_id,),
    ).fetchone()
    assert row[0] == "error"
    assert row[1] == "collector timeout"


def test_no_get_endpoint_for_ingest_signal(client):
    response = client.get("/ingest/signal")
    assert response.status_code == 405
