from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy import select

from src.models.message import Message
from pyrogram.types import Message as TelegramMessage


async def save_messages(messages: list[TelegramMessage], session: AsyncSession):
    if not messages:
        return

    for telegram_message in messages:
        text = telegram_message.text or telegram_message.caption or ""
        if not text:
            continue

        message = Message(
            text=text,
            with_media=telegram_message.media is not None,
            message_id=telegram_message.id,
            channel_id=telegram_message.chat.id,
            created_at=telegram_message.date
        )
        session.add(message)

    await session.commit()


async def get_last_message_datetime(channel_id: int, session: AsyncSession) -> str | None:
    result = await session.execute(
        select(Message.created_at)
        .where(Message.channel_id == channel_id)
        .order_by(Message.created_at.desc())
        .limit(1)
    )
    last_message = result.scalar_one_or_none()
    return last_message
