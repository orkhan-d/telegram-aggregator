from telethon import TelegramClient
from telethon.types import Message

from core.settings import settings


async def process_message_media(client: TelegramClient, message: Message) -> str | None:
    if client.is_connected():
        if not message.media:
            return None
        elif message.media.photo or message.media.video or message.media.document:
            path = await client.download_media(message, settings.userbot.full_download_folder)
            return path.split('/')[-1]

        await client.disconnect()
        return None
    else:
        return None
