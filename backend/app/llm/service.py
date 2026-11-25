from collections.abc import AsyncGenerator

from app.core.config import get_settings
from app.llm.ollama_provider import OllamaProvider
from app.llm.schemas import ChatMessage


class LLMService:
    def __init__(self) -> None:
        settings = get_settings()

        self.provider_name = settings.model_provider
        self.provider = self._create_provider()

    def _create_provider(self) -> OllamaProvider:
        if self.provider_name == "ollama":
            return OllamaProvider()

        raise ValueError(
            f"Unsupported LLM provider: {self.provider_name}"
        )

    async def chat(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
    ) -> str:
        return await self.provider.chat(
            messages=messages,
            temperature=temperature,
        )

    async def stream_chat(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        async for chunk in self.provider.stream_chat(
            messages=messages,
            temperature=temperature,
        ):
            yield chunk