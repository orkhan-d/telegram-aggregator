from beanie import Document
from pydantic import BaseModel
from datetime import datetime as dt


class Channel(BaseModel):
    channel_id: int
    title: str


class Message(Document):
    text: str
    media: list[str]
    message_id: int
    channel: Channel | None
    created_at: dt

    class Settings:
        name = "messages"

    def __str__(self) -> str:
        channel_id = self.channel.channel_id
        if not channel_id:
            return self.text

        if str(channel_id).startswith("-100"):
            channel_id = abs(int(str(channel_id)[4:]))

        return f"{self.text}\n\nhttps://t.me/c/{channel_id}/{self.message_id}"