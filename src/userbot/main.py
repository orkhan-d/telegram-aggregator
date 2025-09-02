import asyncio
import aiocron

from core.db import init_db
from core.settings import settings

from src.userbot.utils import proceed_message_media
from src.userbot.crud import get_last_message_created_at
from src.userbot.userbot import userbot

from src.models.message import Message, Channel
from src.userbot.crud import save_messages


@aiocron.crontab("*/5 * * * *")
async def scheduled_read_channels() -> None:
    if userbot.reading:
        return
    userbot.reading = True

    for channel_id in userbot.channel_ids:
        last_datetime = await get_last_message_created_at(channel_id)
        db_messages = []

        await userbot.start()

        messages = await userbot.read_channel(channel_id, last_datetime)

        while len(messages):
            message = messages.pop(0)
            media_group = [message]
            while len(messages) and messages[0].media_group_id == message.media_group_id:
                media_group.append(messages.pop(0))

            text = message.text or message.caption or ""
            media = []
            for msg in media_group:
                filename = await proceed_message_media(msg)
                media.append(f'{settings.userbot.full_download_folder}/{filename}')

            channel = Channel(
                channel_id=channel_id,
                title=message.chat.title
            )

            db_messages.append(Message(
                text=text,
                media=media,
                message_id=message.id,
                channel=channel,
                created_at=message.date
            ))

        await userbot.stop()

        await save_messages(db_messages)

        await asyncio.sleep(10)

    userbot.reading = False


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init_db())
    asyncio.get_event_loop().run_until_complete(userbot.init())
    asyncio.get_event_loop().run_forever()
