from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(
        description="Message role: system, user, or assistant"
    )

    content: str


class ChatRequest(BaseModel):
    messages: list[ChatMessage]

    temperature: float = Field(
        default=0.7,
        ge=0.0,
        le=2.0,
    )

    stream: bool = False


class ChatResponse(BaseModel):
    message: ChatMessage

    model: str

    provider: str

    done: bool = True