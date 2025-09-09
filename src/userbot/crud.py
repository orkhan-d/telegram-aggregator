from telethon.types import Chat
from src.models.message import Message, Channel as ChannelModel
from datetime import datetime as dt, UTC


async def create_message(text: str, media: list[str],
                         chat: Chat, message_id: int) -> str | None:
    message = Message(
        text=text,
        media=media,
        message_id=message_id,
        channel=ChannelModel(channel_id=chat.id,
                             title=chat.title),
        created_at=dt.now(UTC)
    )
    await message.save()
