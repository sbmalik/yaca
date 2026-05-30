from pathlib import Path
import asyncio
from collections.abc import AsyncIterable
from datetime import datetime
from uuid import UUID

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.sse import EventSourceResponse, ServerSentEvent
from loguru import logger
from pydantic import BaseModel, ConfigDict
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from config.config import config
from db.models import ChatMessage, Conversation
from db.session import get_session
from llm.llm_chat import chat_response

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class UserMessage(BaseModel):
    message: str


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


STATIC_DIR = Path(__file__).parent / "static"


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/conversations", response_model=list[ConversationOut])
async def list_conversations(
    user_id: int = 1,
    session: AsyncSession = Depends(get_session),
) -> list[Conversation]:
    result = await session.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
    )
    return list(result.scalars().all())


@app.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[ChatMessageOut],
)
async def list_conversation_messages(
    conversation_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> list[ChatMessage]:
    result = await session.execute(
        select(ChatMessage)
        .where(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at.asc())
    )
    return list(result.scalars().all())


@app.post("/chat/stream", response_class=EventSourceResponse)
async def sse_items(user_message: UserMessage) -> AsyncIterable[ServerSentEvent]:
    logger.info(f"User message: {user_message.message}")
    yield ServerSentEvent(event="AI", data="__START__")
    async for chunk in chat_response(
        messages=[
            {
                "role": "user",
                "content": user_message.message,
            }
        ]
    ):
        if config.mock_response:
            await asyncio.sleep(0.2)
        yield ServerSentEvent(event="AI", data=chunk)
    yield ServerSentEvent(event="AI", data="__END__")
