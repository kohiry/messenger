from typing import Annotated
from fastapi import APIRouter, Depends, Query, File, UploadFile, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.constants import MediaEnum
from app.auth.services import get_current_user
from app.chat.constants import CORE_PATH_STATIC
from app.chat.orm import (
    get_chat,
    get_chat_id_by_friend_id,
    create_chat_by_friend_id,
    get_chats_by_current_user,
    create_message_by_recipient_id,
)
from app.chat.schemas import ChatSchema, AnswerGood
from app.chat.services import create_folder, get_logger, save_media
from app.errors import get_404_user_not_found
from app.session import get_async_session
from app.user.orm import get_user_by_id
from app.user.schemas import UserOut


chat_router = APIRouter(prefix="/chat", tags=["Messanger"])


# @chat_router.get("/id/{chat_id}")
async def get_chat_by_id(
    chat_id: int,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
) -> ChatSchema | None:
    chat = await get_chat(chat_id, current_user.id, session)
    return chat


# @chat_router.get("/my")
async def get_my_chats(
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
) -> list[ChatSchema]:
    return await get_chats_by_current_user(current_user.id, session)


# @chat_router.post("/start_with")
async def start_chat_with_friend(
    friend_id: Annotated[int, Query()],
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
) -> int:
    friend_account = await get_user_by_id(friend_id, session)
    if friend_account is None:
        raise get_404_user_not_found()
    chat_id = await get_chat_id_by_friend_id(friend_id, current_user.id, session)
    if chat_id is not None:
        return chat_id
    return await create_chat_by_friend_id(friend_id, current_user.id, session)


# @chat_router.post("/send_message/text")
async def send_message(
    text: str,
    chat_id: int,
    current_user: Annotated[UserOut, Depends(get_current_user)],
    session: AsyncSession = Depends(get_async_session),
):
    return await create_message_by_recipient_id(
        current_user.id, chat_id, session, text
    )


# @chat_router.post("/send_message/media")
async def send_audio(
    media: Annotated[UploadFile, File()],
    current_user: Annotated[UserOut, Depends(get_current_user)],
    type_media: Annotated[MediaEnum, Body()],
    session: AsyncSession = Depends(get_async_session),
):
    chat_logger = get_logger()
    #TODO сделать проверку, нету ли аудио в бд
    folder = CORE_PATH_STATIC + str(current_user.id) + '/' + type_media.name
    filename = folder + '/' + media.filename
    await create_folder(folder)
    chat_logger.info(f"Создана директория юзера {current_user.username}")
    await save_media(media, filename)
    chat_logger.info(f"Файл успешно сохранён в директории {folder}")

    # добавление в базу данных
    # отправка сообщения в брокер для распила на текст

    return AnswerGood()



