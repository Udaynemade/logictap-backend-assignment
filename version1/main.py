from typing import Annotated

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, StringConstraints

app = FastAPI(title="Call Records Service")

# In-memory store: call_id -> record (cleared on restart)
calls: dict[str, dict] = {}


class CallEnded(BaseModel):
    call_id: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    status: str
    duration_secs: int = Field(ge=0)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Return a clear, readable error instead of FastAPI's default 422 payload."""
    details = []
    for err in exc.errors():
        field = ".".join(str(p) for p in err["loc"] if p != "body") or "body"
        message = "is required" if err["type"] == "missing" else err["msg"]
        details.append({"field": field, "message": f"{field} {message}"})
    return JSONResponse(
        status_code=422,
        content={"error": "Invalid request", "details": details},
    )


@app.post("/call-ended")
def call_ended(payload: CallEnded, response: Response):
    record = payload.model_dump()

    # setdefault is atomic: it only stores the record if call_id is not present
    stored = calls.setdefault(record["call_id"], record)

    if stored is record:
        response.status_code = 201
        return {"message": "Call record stored", "duplicate": False, "call": stored}

    # Same call_id seen before: keep the original, still return success
    response.status_code = 200
    return {"message": "Call already recorded", "duplicate": True, "call": stored}


@app.get("/calls/{call_id}")
def get_call(call_id: str):
    record = calls.get(call_id)
    if record is None:
        raise HTTPException(status_code=404, detail=f"Call '{call_id}' not found")
    return record