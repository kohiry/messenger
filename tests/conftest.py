import httpx
import pytest
from pydantic_settings import BaseSettings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.auth.schemas import TokenOut
from app.config import settings
from app.user.schemas import UserSchema

DATABASE_URL = (
        f"{settings.P_DRIVER}://{settings.P_USER}:{settings.P_PASS}"
        f"@test_postgres:5432/test_{settings.P_DB}"
    )


class Settings(BaseSettings):
    username1: str
    password1: str
    username2: str
    password2: str
    email1: str
    email2: str

    class Config:
        env_file = '.env.test'


settings = Settings()


@pytest.fixture(scope="session")
def _create_test_users() -> None:
    url = "http://localhost:8000/api/user/register"

    data = {
        "username": settings.username1,
        "password": settings.password1,
        "email": settings.email1
    }
    httpx.post(url=url, data=data)
    data = {
        "username": settings.username2,
        "password": settings.password2,
        "email": settings.email2
    }
    httpx.post(url=url, data=data)


@pytest.fixture(scope="session")
def _session() -> Session:

    engine = create_engine(DATABASE_URL)

    session_maker = sessionmaker(engine, expire_on_commit=False)

    return session_maker()


@pytest.fixture(scope="session")
def _get_tokens(_create_test_users) -> list[TokenOut]:
    url = "http://localhost:8000/api/security/token"

    data = {
        "username": settings.username1,
        "password": settings.password1,
    }
    data2 = {
        "username": settings.username2,
        "password": settings.password2,
    }
    response = httpx.post(url=url, data=data)
    response2 = httpx.post(url=url, data=data2)
    t_1 = TokenOut.model_validate(response.json())
    t_2 = TokenOut.model_validate(response2.json())
    return [t_1, t_2]

