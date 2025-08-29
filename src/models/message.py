from beanie import Document
from pydantic import BaseModel
from datetime import datetime as dt


class Channel(BaseModel):
    channel_id: int
    title: str


class Message(Document):
    text: str
    media: list[str] | str | None
    message_id: int
    channel: Channel | None
    created_at: dt

    class Settings:
        name = "messages"
