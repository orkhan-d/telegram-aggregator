from telethon import TelegramClient
from telethon.tl.functions.messages import GetDialogFiltersRequest
from telethon.tl.types.messages import DialogFilters
from telethon.tl.types import DialogFilter, DialogFilterChatlist, InputPeerChannel

from core.settings import settings


class Userbot:
    channel_ids: set[int]
    reading: bool = False

    def __init__(self) -> None:
        self.channel_ids = set()
        self.client: TelegramClient = TelegramClient(
            session='telegram-aggregator',
            api_id=settings.userbot.api_id,
            api_hash=settings.userbot.api_hash,
        )

    async def init(self):
        await self.client.connect()
        self.channel_ids.update(settings.userbot.channel_ids)
        await self._get_channels_from_folders()

    async def _get_channels_from_folders(self):
        if settings.userbot.folder_names:
            folder_names = list(map(lambda n: n.lower(), settings.userbot.folder_names))

            res: DialogFilters = await self.client(GetDialogFiltersRequest())
            for dialog_filter in res.filters:
                if isinstance(dialog_filter, DialogFilter) or isinstance(dialog_filter, DialogFilterChatlist):
                    if dialog_filter.title.text.lower() in folder_names:
                        for peer in dialog_filter.include_peers:
                            if isinstance(peer, InputPeerChannel):
                                self.channel_ids.add(int(f'-100{peer.channel_id}'))

            await self.client.disconnect()


userbot = Userbot()
