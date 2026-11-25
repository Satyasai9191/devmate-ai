from collections.abc import AsyncGenerator

import httpx

from app.core.config import get_settings
from app.llm.schemas import ChatMessage


class OllamaError(Exception):
    """Raised when communication with Ollama fails."""


class OllamaProvider:
    def __init__(self) -> None:
        settings = get_settings()

        self.base_url = settings.ollama_base_url.rstrip("/")
        self.model = settings.model_name

    async def chat(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
    ) -> str:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in messages
            ],
            "stream": False,
            "options": {
                "temperature": temperature,
            },
        }

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(
                    connect=10.0,
                    read=120.0,
                    write=30.0,
                    pool=30.0,
                )
            ) as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                )

                response.raise_for_status()

                data = response.json()

                return data["message"]["content"]

        except httpx.HTTPError as exc:
            raise OllamaError(
                f"Failed to communicate with Ollama: {exc}"
            ) from exc

        except (KeyError, TypeError) as exc:
            raise OllamaError(
                "Ollama returned an unexpected response."
            ) from exc

    async def stream_chat(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
    ) -> AsyncGenerator[str, None]:
        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": message.role,
                    "content": message.content,
                }
                for message in messages
            ],
            "stream": True,
            "options": {
                "temperature": temperature,
            },
        }

        try:
            async with httpx.AsyncClient(
                timeout=None
            ) as client:
                async with client.stream(
                    "POST",
                    f"{self.base_url}/api/chat",
                    json=payload,
                ) as response:

                    response.raise_for_status()

                    async for line in response.aiter_lines():
                        if not line:
                            continue

                        import json

                        data = json.loads(line)

                        message = data.get("message", {})
                        content = message.get("content", "")

                        if content:
                            yield content

                        if data.get("done"):
                            break

        except httpx.HTTPError as exc:
            raise OllamaError(
                f"Failed to stream from Ollama: {exc}"
            ) from exc