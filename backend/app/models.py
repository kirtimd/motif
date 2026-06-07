"""ORM models.

Phase 1: a single `items` table — the intent-rich, provenance-tracked corpus
that everything else is built on. See docs/plan.md for the signed-off design.
"""
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Index, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base

# Single-user seed owner until real auth lands. Every row is owned and every
# query is scoped by user_id from day one, so adding real auth later is a clean
# migration, not a retrofit. See the auth-migration checklist in docs/plan.md.
SEED_USER_ID = uuid.UUID("00000000-0000-0000-0000-000000000001")


class Item(Base):
    """A captured spark — a thing that piqued your attention, plus *why*."""

    __tablename__ = "items"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), nullable=False, default=SEED_USER_ID
    )

    # 'url' | 'text' | 'note' — validated in the app, not a rigid DB enum.
    source_type: Mapped[str] = mapped_column(String(20), nullable=False)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    content: Mapped[str | None] = mapped_column(Text, nullable=True)
    excerpt: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(Text, nullable=True)

    # The intent: why this sparked you. The highest-value signal for the loop.
    spark_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    # 'pending' | 'ready' | 'failed' — future-proofs async extraction/embedding.
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="ready")

    # Flexible provenance/metadata: author, site_name, published_at, word_count…
    extra: Mapped[dict] = mapped_column(
        JSONB, nullable=False, default=dict, server_default="{}"
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    # The feed query: this user's sparks, newest first.
    __table_args__ = (Index("ix_items_user_created", "user_id", "created_at"),)
