import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator


app = FastAPI(title="Call Records Service")

DATABASE = "calls.db"


def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS calls (
                call_id TEXT PRIMARY KEY,
                status TEXT NOT NULL,
                duration_secs INTEGER NOT NULL
            )
            """
        )


init_db()


class CallEnded(BaseModel):
    call_id: str
    status: str
    duration_secs: int = Field(ge=0)

    @field_validator("call_id")
    @classmethod
    def validate_call_id(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("call_id is required")

        return value


@app.post("/call-ended")
def call_ended(payload: CallEnded):
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.execute(
            """
            INSERT OR IGNORE INTO calls
            (call_id, status, duration_secs)
            VALUES (?, ?, ?)
            """,
            (
                payload.call_id,
                payload.status,
                payload.duration_secs,
            ),
        )

        if cursor.rowcount == 1:
            return {
                "message": "Call record stored",
                "duplicate": False,
                "call": payload.model_dump(),
            }

        row = conn.execute(
            """
            SELECT call_id, status, duration_secs
            FROM calls
            WHERE call_id = ?
            """,
            (payload.call_id,),
        ).fetchone()

    return {
        "message": "Call already recorded",
        "duplicate": True,
        "call": {
            "call_id": row[0],
            "status": row[1],
            "duration_secs": row[2],
        },
    }


@app.get("/calls/{call_id}")
def get_call(call_id: str):
    with sqlite3.connect(DATABASE) as conn:
        row = conn.execute(
            """
            SELECT call_id, status, duration_secs
            FROM calls
            WHERE call_id = ?
            """,
            (call_id,),
        ).fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail=f"Call '{call_id}' not found",
        )

    return {
        "call_id": row[0],
        "status": row[1],
        "duration_secs": row[2],
    }