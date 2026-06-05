"""Motif API — Phase 0 skeleton.

Just enough to prove the stack is wired together end to end: the frontend can
reach the backend, and the backend can reach the database.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .db import engine

app = FastAPI(title="Motif API", version="0.0.0")

# Allow the Vite dev server (Phase 0 frontend) to call us during development.
# Both hostnames are listed because the browser treats localhost and 127.0.0.1
# as distinct origins, and either may be used to open the app.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    """Liveness + database connectivity in one check."""
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        database = "connected"
    except Exception as exc:  # noqa: BLE001 — surface any DB issue to the caller
        database = f"unreachable: {exc.__class__.__name__}"
    return {"status": "ok", "database": database}
