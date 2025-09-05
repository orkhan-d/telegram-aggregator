import asyncio

from pyrogram import types
from pyrogram.client import Client
from pyrogram.raw.functions.messages import GetDialogFilters
from pyrogram.raw.types import InputPeerChannel
from pyrogram.raw.types.dialog_filter import DialogFilter
from pyrogram.raw.types.dialog_filter_default import DialogFilterDefault

from core.settings import settings
from datetime import datetime as dt


class Userbot:
    channel_ids: set[int]
    reading: bool = False

    def __init__(self) -> None:
        self.channel_ids = set()
        self.client: Client = Client(
            name='telegram-aggregator',
            api_id=settings.userbot.api_id,
            api_hash=settings.userbot.api_hash,
        )

    async def start(self):
        await self.client.start()

    async def stop(self):
        await self.client.stop()

    async def init(self):
        self.channel_ids.update(settings.userbot.channel_ids)
        await self.get_channels_from_folders()

    async def get_channels_from_folders(self):
        if settings.userbot.folder_names:
            folder_names = list(map(lambda n: n.lower(), settings.userbot.folder_names))
            await self.client.start()

            folders: list[DialogFilter | DialogFilterDefault] = await self.client.invoke(GetDialogFilters())
            for folder in folders:
                if hasattr(folder, 'title') and folder.title.lower() in folder_names:
                    peers = folder.include_peers
                    for p in peers:
                        if isinstance(p, InputPeerChannel):
                            channel_id = int(f'-100{p.channel_id}')
                            self.channel_ids.add(channel_id)

            await self.client.stop()

    async def read_channel(self, channel_id: int, last_datatime: dt | None = None) -> list[types.Message]:
        messages: list[types.Message] = []
        offset: int = 0

        while True:
            async for message in self.client.get_chat_history(channel_id, limit=10, offset=offset):
                if message.id in list(map(lambda m: m.id, messages)):
                    continue
                if last_datatime and message.date <= last_datatime:
                    break

                if message.media_group_id:
                    messages += await message.get_media_group()
                else:
                    messages += [message]

            if len(messages) < offset + 10 or last_datatime is None:
                break

            offset += 10
            await asyncio.sleep(10)

        return messages


userbot = Userbot()
