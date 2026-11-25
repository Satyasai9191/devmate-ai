from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.llm.ollama_provider import OllamaError
from app.llm.schemas import ChatRequest, ChatResponse
from app.llm.service import LLMService


router = APIRouter(
    prefix="/chat",
    tags=["Chat"],
)

llm_service = LLMService()


@router.post("", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = await llm_service.chat(
            messages=request.messages,
            temperature=request.temperature,
        )

        return ChatResponse(
            message={
                "role": "assistant",
                "content": response,
            },
            model="qwen3:1.7b",
            provider="ollama",
        )

    except OllamaError as exc:
        raise HTTPException(
            status_code=503,
            detail=str(exc),
        ) from exc


@router.post("/stream")
async def stream_chat(request: ChatRequest):
    async def generate():
        try:
            async for chunk in llm_service.stream_chat(
                messages=request.messages,
                temperature=request.temperature,
            ):
                yield chunk

        except OllamaError as exc:
            yield f"\n[ERROR] {exc}"

    return StreamingResponse(
        generate(),
        media_type="text/plain",
    )