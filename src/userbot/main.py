import asyncio
import aiocron

from core.db import init_db

from src.userbot.utils import get_message_media_file_id
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

        messages = await userbot.read_channel(channel_id, last_datetime)

        channel = Channel(
            channel_id=channel_id,
            title=messages[0].chat.title if len(messages) else ""
        )

        while len(messages):
            message = messages.pop(0)

            if message.media_group_id:
                media_group = [message]
                while len(messages) and messages[0].media_group_id == message.media_group_id:
                    media_group.append(messages.pop(0))

                main_message = media_group[0]
                db_messages.append(Message(
                    text=main_message.text or main_message.caption or "",
                    media=[get_message_media_file_id(m)
                           for m in media_group],
                    message_id=main_message.id,
                    channel=channel,
                    created_at=main_message.date
                ))
            else:
                db_messages.append(Message(
                    text=message.text or message.caption or "",
                    media=get_message_media_file_id(message),
                    message_id=message.id,
                    channel=channel,
                    created_at=message.date
                ))
        await save_messages(db_messages)

        await asyncio.sleep(10)

    userbot.reading = False


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(init_db())
    asyncio.get_event_loop().run_until_complete(userbot.init())
    asyncio.get_event_loop().run_forever()
