from fastapi.security import OAuth2PasswordBearer
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.session import get_async_session

auth_router = APIRouter(prefix='/security')


@auth_router.post('/token')
def new_token(session: AsyncSession = Depends(get_async_session)):
    pass
