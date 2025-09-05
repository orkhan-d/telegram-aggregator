from pyrogram.types import Message

from core.settings import settings


async def proceed_message_media(message: Message) -> str | None:
    if not message.media:
        return None

    if message.photo or message.video or message.document:
        path = await message.download(settings.userbot.full_download_folder)
        return path.split('/')[-1]

    raise Exception("Unsupported media type")
