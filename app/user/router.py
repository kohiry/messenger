from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import get_error_user_in_db, get_error_user_not_create, get_404_user_not_found
from app.session import get_async_session
from app.user.schemas import UserIn, UserOut, CreatedUserMessage
from app.user.orm import create_user, get_user_by_username, get_user_by_id

user_router = APIRouter(prefix='/user')


@user_router.get('/profile/me')
def user_me() -> dict:
    return {'user': 'cool user'}


@user_router.post('/register')
async def user_register(user: UserIn, session: AsyncSession = Depends(get_async_session)) -> CreatedUserMessage:
    get_user = await get_user_by_username(user.username, session)
    if get_user is None:
        raise get_error_user_in_db()
    new_user = await create_user(user, session)
    return new_user


@user_router.get('/profile/{user_id}')
async def user_profile(user_id: int, session: AsyncSession = Depends(get_async_session)) -> UserOut:
    get_user = await get_user_by_id(user_id, session)
    if get_user is None:
        raise get_404_user_not_found()
    return get_user

