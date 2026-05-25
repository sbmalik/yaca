from langchain.chat_models import init_chat_model
from collections.abc import AsyncIterable

from config.config import config

MOCK_RESPONSE = "This is a mock response"

model = init_chat_model(
    model=f"litellm:{config.model_name}",
    streaming=True,
)


async def chat_response(messages: list[dict]) -> AsyncIterable[str]:
    async for chunk in model.astream(
        messages,
        mock_response=MOCK_RESPONSE if config.mock_response else None,
    ):
        yield chunk.content
