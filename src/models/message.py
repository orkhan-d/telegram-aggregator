from core.db import Base, UuidPkMixin, TimestampsMixin
from sqlalchemy.orm import Mapped, mapped_column


class Message(Base, UuidPkMixin, TimestampsMixin):
    __tablename__ = "messages"

    text: Mapped[str | None] = mapped_column()
    with_media: Mapped[bool] = mapped_column()
    message_id: Mapped[int] = mapped_column()
    channel_id: Mapped[int] = mapped_column()