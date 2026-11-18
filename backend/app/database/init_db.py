import asyncio

from app.database.base import Base
from app.database.models import Conversation
from app.database.session import engine


async def init_database() -> None:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    print("Database initialized successfully.")


if __name__ == "__main__":
    asyncio.run(init_database())