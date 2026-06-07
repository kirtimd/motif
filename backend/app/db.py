"""Database setup: engine, session factory, and the declarative Base.

- `engine` — the connection pool to Postgres.
- `SessionLocal` — call it to get a short-lived DB session per request.
- `Base` — parent class all ORM models inherit from; its `.metadata` is what
  Alembic diffs against the live database to generate migrations.
"""
import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://motif:motif@localhost:5432/motif",
)

# pool_pre_ping avoids handing out dead connections after the DB restarts.
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()
