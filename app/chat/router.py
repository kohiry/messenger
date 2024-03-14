from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.services import get_current_user
from app.chat.orm import get_chat, get_chat_id_by_friend_id, create_chat_by_friend_id, get_chats_by_current_user
from app.chat.schemas import ChatSchema
from app.errors import get_404_user_not_found
from app.session import get_async_session
from app.user.orm import get_user_by_id
from app.user.schemas import UserOut


chat_router = APIRouter(prefix='/chat', tags=["Messanger"])


@chat_router.get('/id/{chat_id}')
async def get_chat_by_id(
        chat_id: int,
        current_user: Annotated[UserOut, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
) -> ChatSchema | None:
    chat = await get_chat(chat_id, current_user.id, session)
    return chat


@chat_router.get("/my")
async def get_my_chats(
        current_user: Annotated[UserOut, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
) -> list[ChatSchema]:
    return await get_chats_by_current_user(current_user.id, session)


@chat_router.post("/start_with")
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

