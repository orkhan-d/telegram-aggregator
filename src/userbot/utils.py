from pyrogram.types import Message
from pyrogram.enums import MessageMediaType


def get_message_media_file_id(message: Message) -> str | None:
    match message.media:
        case MessageMediaType.PHOTO:
            return message.photo.file_id
        case MessageMediaType.VIDEO:
            return message.video.file_id
        case MessageMediaType.ANIMATION:
            return message.animation.file_id
        case MessageMediaType.VOICE:
            return message.voice.file_id
        case MessageMediaType.AUDIO:
            return message.audio.file_id
        case MessageMediaType.DOCUMENT:
            return message.document.file_id
        case _:
            return None
