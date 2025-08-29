from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from core.settings import settings
from src.models import models

client = AsyncIOMotorClient(settings.db.url)
db = client[settings.db.name]


async def init_db():
    await init_beanie(database=db, document_models=models)

    await db["messages"].create_index(
        [("channel_id", 1), ("message_id", 1)], unique=True
    )
