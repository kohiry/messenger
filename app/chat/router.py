from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.services import get_current_user
from app.chat.schemas import ChatSchema
from app.chat.service import get_chat
from app.session import get_async_session
from app.user.schemas import UserOut


chat_router = APIRouter(prefix='/chat', tags=["Messanger"])


@chat_router.get('/{chat_id}')
def get_all_chat(
        chat_id: int,
        current_user: Annotated[UserOut, Depends(get_current_user)],
        session: AsyncSession = Depends(get_async_session),
):
    chat = get_chat(chat_id, current_user.id, session)

