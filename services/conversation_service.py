from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from constants import Role
from db.models import ChatMessage, Conversation


async def get_conversations(session: AsyncSession, user_id: int) -> list[Conversation]:
    result = await session.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
    )
    return list(result.scalars().all())


async def get_messages(
    session: AsyncSession, conversation_id: UUID
) -> list[ChatMessage]:
    result = await session.execute(
        select(ChatMessage)
        .where(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at.asc())
    )
    return list(result.scalars().all())


async def create_chat_message(
    session: AsyncSession,
    conversation_id: UUID,
    role: Role,
    content: str,
):
    session.add(
        ChatMessage(
            conversation_id=conversation_id,
            role=role,
            content=content,
        )
    )
    await session.commit()


def make_title(message: str) -> str:
    return message if len(message) <= 30 else f"{message[:30]}..."


async def start_turn(
    session: AsyncSession, conversation_id: UUID, user_id: int, message: str
):
    conversation = await session.get(Conversation, conversation_id)
    is_new = conversation is None
    if is_new:
        session.add(
            Conversation(
                id=conversation_id,
                user_id=user_id,
                title=make_title(message),
            )
        )
        await session.flush()
    history = (
        []
        if is_new
        else [
            {"role": m.role, "content": m.content}
            for m in await get_messages(session, conversation_id)
        ]
    )
    session.add(
        ChatMessage(
            conversation_id=conversation_id,
            role=Role.USER,
            content=message,
        )
    )
    await session.commit()
    return history + [{"role": Role.USER, "content": message}]
