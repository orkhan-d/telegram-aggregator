import asyncio

import aiocron
from core.db import get_session
from src.userbot.crud import save_messages, get_last_message_datetime
from src.userbot.userbot import userbot


@aiocron.crontab("* * * * *")
async def scheduled_read_channels() -> None:
    if userbot.reading:
        return
    userbot.reading = True

    for channel_id in userbot.channel_ids:
        async with get_session() as session:
            last_datetime = await get_last_message_datetime(channel_id, session)

        messages = await userbot.read_channel(channel_id, last_datetime)
        async with get_session() as session:
            await save_messages(messages, session)

        await asyncio.sleep(10)

    userbot.reading = False


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(userbot.init())
    asyncio.get_event_loop().run_forever()
