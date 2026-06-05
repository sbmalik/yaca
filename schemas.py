from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class UserMessage(BaseModel):
    message: str = Field(min_length=1)
    conversation_id: UUID


class ConversationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    user_id: int
    title: str
    created_at: datetime


class ChatMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    conversation_id: UUID
    role: str
    content: str
    created_at: datetime
