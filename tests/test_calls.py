import os
import sqlite3

from fastapi.testclient import TestClient

from final.main import app


client = TestClient(app)


def test_duplicate_call_is_not_stored_twice():
    call_id = "test-duplicate-001"

    with sqlite3.connect("calls.db") as conn:
        conn.execute("DELETE FROM calls WHERE call_id = ?", (call_id,))
        conn.commit()

    payload = {
        "call_id": call_id,
        "status": "answered",
        "duration_secs": 42,
    }

    first_response = client.post("/call-ended", json=payload)
    second_response = client.post("/call-ended", json=payload)

    assert first_response.status_code == 200 or first_response.status_code == 201
    assert second_response.status_code == 200
    assert second_response.json()["duplicate"] is True

    with sqlite3.connect("calls.db") as conn:
        count = conn.execute(
            "SELECT COUNT(*) FROM calls WHERE call_id = ?",
            (call_id,),
        ).fetchone()[0]

    assert count == 1
    