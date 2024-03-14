from sqlalchemy import select, or_, and_, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.chat.models import Chat, Message
from app.chat.schemas import ChatSchema, MessageSchema


async def get_messages_by_chat_id(chat_id: int, session: AsyncSession) -> list[MessageSchema]:
    messages = (
        await session.execute(
            select(Message).where(
                Message.chat_id == chat_id
            )
        )
    ).scalars()

    if messages is None:
        return []

    return [MessageSchema.model_validate(message.get_dict()) for message in messages]


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

    schema_messages = await get_messages_by_chat_id(chat.id, session)
    chat_dict = chat.get_dict()
    chat_dict.update({'messages': schema_messages})

    return ChatSchema.model_validate(chat_dict)


async def get_chat_id_by_friend_id(friend_id: int, user_id: int, session: AsyncSession) -> None | int:
    return (
        await session.execute(
            select(func.coalesce(Chat.id, None)).where(
                or_(
                    and_(
                        Chat.first_user_id == user_id,
                        Chat.second_user_id == friend_id,
                    ),
                    and_(
                        Chat.first_user_id == friend_id,
                        Chat.second_user_id == user_id,
                    ),
                )
            )
        )
    ).scalar_one_or_none()


async def create_chat_by_friend_id(friend_id: int, user_id: int, session: AsyncSession) -> int:
    chat = Chat(
        first_user_id=user_id,
        second_user_id=friend_id
    )
    session.add(chat)
    await session.commit()
    return chat.id


async def get_chats_by_current_user(current_id: int, session: AsyncSession):
    chats = (
        await session.execute(
            select(Chat).where(
                or_(
                    Chat.first_user_id == current_id,
                    Chat.second_user_id == current_id
                )
            )
        )
    ).scalars()

    chats_schemas: list[ChatSchema] = []

    for chat in chats:  # use async for bruh
        schema_messages = await get_messages_by_chat_id(chat.id, session)
        chat_dict = chat.get_dict()
        chat_dict.update({'messages': schema_messages})  # TODO usless
        if chat_dict is None:
            continue
        chats_schemas.append(ChatSchema.model_validate(chat_dict))

    return chats_schemas


async def create_message_by_recipient_id(
        sender_id: int, chat_id: int, session: AsyncSession,
        text: str
) -> int | None:
    chat = (await session.execute(
        select(Chat).where(
            and_(
                or_(Chat.first_user_id == sender_id, Chat.second_user_id == sender_id),
                Chat.id == chat_id
            )
        )
    )).scalar_one_or_none()
    if chat is None:
        return None
    recipient_id = chat.second_user_id != sender_id and chat.second_user_id or chat.first_user_id
    message = Message(chat_id=chat_id, sender_id=sender_id, recipient_id=recipient_id,
                      text=text)
    session.add(message)
    await session.commit()
    return message.id



