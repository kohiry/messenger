from sqlalchemy import select, or_, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.models import Chat, Message
from app.chat.schemas import ChatSchema, MessageSchema


async def get_chat(chat_id: int, user_id: int, session: AsyncSession) -> ChatSchema | None:
    chat = (
        await session.execute(
            select(Chat).where(
                and_(
                    Chat.id == chat_id,
                    or_(Chat.first_user_id == user_id, Chat.second_user_id == user_id),
                )
            )
        )
    ).scalar_one_or_none()
    if not chat:
        return None

    messages = (
        await session.execute(
            select(Message).where(
                Message.chat_id == chat_id
            )
        )
    ).scalars()

    if messages is None:
        return ChatSchema.model_validate(**chat.get_dict())

    schema_messages = [MessageSchema.model_validate(**message.get_dict()) for message in messages]
    print(schema_messages)

    return ChatSchema.model_validate(**chat.get_dict(), messages=schema_messages)


