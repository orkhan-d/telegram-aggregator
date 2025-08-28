from core.db import Base, UuidPkMixin
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime as dt
from sqlalchemy import BIGINT


class Message(Base, UuidPkMixin):
    __tablename__ = "messages"

    text: Mapped[str | None] = mapped_column()
    with_media: Mapped[bool] = mapped_column()
    message_id: Mapped[int] = mapped_column(type_=BIGINT)
    channel_id: Mapped[int] = mapped_column(type_=BIGINT)
    created_at: Mapped[dt] = mapped_column()
