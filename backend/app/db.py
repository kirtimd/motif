"""Database connection setup.

A single SQLAlchemy engine for the whole app. We'll add ORM models here in
Phase 1 when we start persisting captured items.
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://motif:motif@localhost:5432/motif",
)

# pool_pre_ping avoids handing out dead connections after the DB restarts.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
