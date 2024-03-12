from datetime import datetime

import pytest

from app.auth.schemas import TokenOut, TokenIn
from app.auth.services import jwt_code, jwt_decode


def test_schemas_auth():
    t = TokenOut(access_token='zxc')
    assert t.access_token == 'zxc'
    assert t.token_type == 'bearer'
    time = datetime.now()
    t2 = TokenIn(sub='zxc', exp=time)
    assert t2.sub == 'zxc'
    assert t2.exp == time


def test_jwt():
    username = 'zxc'
    token_out = jwt_code(username)
    assert token_out.access_token != username
    assert jwt_decode(token_out.access_token).sub == username
