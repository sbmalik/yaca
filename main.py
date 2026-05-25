from pathlib import Path
import asyncio
from collections.abc import AsyncIterable

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.sse import EventSourceResponse, ServerSentEvent
from loguru import logger
from pydantic import BaseModel
from config.config import config
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


STATIC_DIR = Path(__file__).parent / "static"


@app.get("/")
async def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


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
