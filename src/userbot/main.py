import asyncio

from telethon import events

from core.db import init_db

from telethon.types import Chat
from telethon.tl.patched import Message

from src.userbot.userbot import userbot
from src.userbot.utils import process_message_media
from src.userbot.crud import create_message


async def on_new_message(event: events.NewMessage.Event):
    message: Message = event.message
    chat: Chat = await event.get_chat()

    print("New message from", chat.title)

    path = await process_message_media(userbot.client, message)
    if not path:
        media = []
    else:
        media = [path]
    text = message.message or ""
    await create_message(text, media, chat, message.id)


async def on_album(event: events.Album.Event):
    messages: list[Message] = event.messages
    chat: Chat = await event.get_chat()

    print("New album from", chat.title)

    media = []
    for message in messages:
        path = await process_message_media(userbot.client, message)
        if path:
            media.append(path)

    await create_message(event.text, media, chat, messages[0].id)


async def main():
    await init_db()
    await userbot.init()

    userbot.client.add_event_handler(on_album, events.Album(chats=userbot.channel_ids))
    userbot.client.add_event_handler(on_new_message, events.NewMessage(chats=userbot.channel_ids))

    print("Running userbot...")

    await userbot.client.start()
    await userbot.client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
