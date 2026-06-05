from uuid import UUID

from fastapi import APIRouter, Depends

import schemas
from db import models
from db.session import get_session
from services import conversation_service

router = APIRouter()


@router.get("/conversations", response_model=list[schemas.ConversationOut])
async def list_conversations(user_id: int = 1, session=Depends(get_session)):
    return await conversation_service.get_conversations(session, user_id)


@router.get(
    "/conversations/{conversation_id}/messages",
    response_model=list[schemas.ChatMessageOut],
)
async def list_conversation_messages(
    conversation_id: UUID,
    session=Depends(get_session),
) -> list[models.ChatMessage]:
    return await conversation_service.get_messages(
        session=session,
        conversation_id=conversation_id,
    )
