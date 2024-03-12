import pytest
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from app.errors import get_error_user_in_db, get_error_user_not_create, get_error_user_not_authenticate, \
    get_404_user_not_found
from app.main import app
from app.session import get_async_session


client = TestClient(app)


@pytest.mark.asyncio
async def test_session():
    session = await anext(get_async_session())
    assert isinstance(session, AsyncSession)


def test_error_user_in_db():
    res = get_error_user_in_db()
    assert isinstance(res, HTTPException)
    assert res.status_code == 401
    assert res.detail == "User actually created"


def test_error_user_not_created():
    res = get_error_user_not_create()
    assert isinstance(res, HTTPException)
    assert res.status_code == 401
    assert res.detail == "Same User data in service"


def test_error_user_not_auth():
    res = get_error_user_not_authenticate()
    assert isinstance(res, HTTPException)
    assert res.status_code == 401
    assert res.detail == "Login User failed"


def test_error_user_not_found():
    res = get_404_user_not_found()
    assert isinstance(res, HTTPException)
    assert res.status_code == 404
    assert res.detail == "User not found"


def test_main():
    response = client.get("/")
    assert response.status_code == 401
    assert response.json() != {"msg": "Hello World"}
