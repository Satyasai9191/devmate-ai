from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import Conversation
from app.database.session import get_db

router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"],
)


@router.post("")
async def create_conversation(
    db: AsyncSession = Depends(get_db),
):
    conversation = Conversation()

    db.add(conversation)
    await db.commit()
    await db.refresh(conversation)

    return {
        "id": str(conversation.id),
        "title": conversation.title,
        "created_at": conversation.created_at,
    }


@router.get("")
async def list_conversations(
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Conversation).order_by(
            Conversation.created_at.desc()
        )
    )

    conversations = result.scalars().all()

    return [
        {
            "id": str(item.id),
            "title": item.title,
            "created_at": item.created_at,
        }
        for item in conversations
    ]


@router.get("/{conversation_id}")
async def get_conversation(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Conversation).where(
            Conversation.id == conversation_id
        )
    )

    conversation = result.scalar_one_or_none()

    if conversation is None:
        return {
            "error": "Conversation not found",
        }

    return {
        "id": str(conversation.id),
        "title": conversation.title,
        "created_at": conversation.created_at,
    }