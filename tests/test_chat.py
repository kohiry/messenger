import httpx
import pytest

from app.auth.schemas import TokenOut
from app.chat.schemas import ChatSchema, MessageSchema
from app.user.schemas import UserSchema, UserOut


def get_header(token: TokenOut) -> dict:
    header = {'Authorization':  token.token_type.title()
                                + ' ' + token.access_token,
              'accept': 'application/json'
              }

    return header


def get_user(token: TokenOut) -> UserOut:
    url_me = "http://localhost:8000/api/user/profile/me"
    header = get_header(token)
    response = httpx.get(url_me, headers=header)
    return UserOut.model_validate(response.json())


def test_create_chat(_get_tokens: list[TokenOut]):
    assert _get_tokens is not None
    url_create_chat = "http://localhost:8000/api/chat/start_with?"
    url_create_chat += f'friend_id={get_user(_get_tokens[1]).id}'
    header = get_header(_get_tokens[0])

    response = httpx.post(url_create_chat, headers=header)
    assert response.status_code == 200
    assert type(response.json()) is int


def test_get_chats_and_send_message(_get_tokens: list[TokenOut]):
    assert _get_tokens is not None
    url_my_chat = "http://localhost:8000/api/chat/my"
    header = get_header(_get_tokens[0])
    response = httpx.get(url_my_chat, headers=header)
    assert response.status_code == 200
    answers = response.json()
    assert type(answers) is list
    chats = [ChatSchema.model_validate(answer) for answer in answers]
    assert type(chats[0]) is ChatSchema
    assert type(chats[0].messages) is list
    assert type(chats[0].messages[0]) is MessageSchema
    url_my_chat = "http://localhost:8000/api/chat/send_message?"
    url_my_chat += f"text=test message&chat_id={chats[0].id}"

    response = httpx.post(url_my_chat, headers=header)
    assert response.status_code == 200
    assert type(response.json()) is int

