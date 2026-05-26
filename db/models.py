from datetime import datetime
from uuid import uuid4

from db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import DateTime, UUID, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.types import Text


class Conversation(Base):
    __tablename__ = "conversations"

    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[UUID] = mapped_column(
        UUID, primary_key=True, default=lambda: str(uuid4())
    )
    conversation_id: Mapped[UUID] = mapped_column(UUID, ForeignKey("conversations.id"))
    role: Mapped[str] = mapped_column(String(10))
    content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
