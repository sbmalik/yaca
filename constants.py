from enum import StrEnum


class Role(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"


SSE_START = "__START__"
SSE_END = "__END__"
SSE_ERROR = "__ERROR__"
SSE_EVENT_NAME = "AI"
