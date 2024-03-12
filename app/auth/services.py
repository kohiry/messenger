from typing import Annotated
from fastapi import Depends
import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import Token
from app.session import get_async_session
from app.auth.constants import oauth2_scheme


def jwt_code(username: str) -> Token:
    pass


def jwt_decode(token: str) -> str:
    pass


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                     session: AsyncSession = Depends(get_async_session)):
    username = jwt_decode(token)


def hash_password(password: str) -> str:
    return password


def compare_password(password: str, hashed_password: str) -> bool:
    return password == hashed_password


