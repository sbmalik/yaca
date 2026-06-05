import asyncio
from collections.abc import AsyncIterable

from fastapi import APIRouter
from fastapi.sse import EventSourceResponse, ServerSentEvent
from loguru import logger

import constants
from config.config import config
from db.session import session_scope
from llm.llm_chat import chat_response
from schemas import UserMessage
from services.conversation_service import create_chat_message, start_turn

router = APIRouter()


@router.post("/chat/stream", response_class=EventSourceResponse)
async def stream_chat(
    user_message: UserMessage,
) -> AsyncIterable[ServerSentEvent]:
    async with session_scope() as session:
        messages = await start_turn(
            session=session,
            conversation_id=user_message.conversation_id,
            user_id=1,
            message=user_message.message,
        )
    logger.info(f"{messages=}")
    yield ServerSentEvent(
        event=constants.SSE_EVENT_NAME,
        data=constants.SSE_START,
    )
    ai_message = ""
    try:
        async for chunk in chat_response(
            messages=messages,
        ):
            if config.mock_response:
                await asyncio.sleep(0.2)
            ai_message += chunk
            yield ServerSentEvent(
                event=constants.SSE_EVENT_NAME,
                data=chunk,
            )
        yield ServerSentEvent(
            event=constants.SSE_EVENT_NAME,
            data=constants.SSE_END,
        )
    except Exception:
        logger.exception("chat stream failed")
        yield ServerSentEvent(event=constants.SSE_EVENT_NAME, data=constants.SSE_ERROR)
    finally:
        if ai_message:
            async with session_scope() as session:
                await create_chat_message(
                    session=session,
                    conversation_id=user_message.conversation_id,
                    role=constants.Role.ASSISTANT,
                    content=ai_message,
                )
