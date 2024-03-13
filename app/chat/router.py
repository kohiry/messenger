from typing import Annotated
from fastapi import APIRouter, Depends
from app.auth.services import get_current_user
from app.user.schemas import UserOut


chat_router = APIRouter(prefix='/chat')


@chat_router.get('/{chat_id}')
def get_all_chat(
        current_user: Annotated[UserOut, Depends(get_current_user)], chat_id: int
):
    pass
