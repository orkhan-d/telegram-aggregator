from src.models.message import Message


async def save_messages(messages: list[Message]) -> None:
    for message in messages:
        await message.insert()


async def get_last_message_created_at(channel_id: int) -> str | None:
    last_message = await (Message
                          .find(Message.channel.channel_id == channel_id)
                          .sort(-Message.created_at).first_or_none())
    return last_message.created_at if last_message else None
