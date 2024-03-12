import pytest

from app.user.services import hash_password, compare_password


def test_hash():
    password = 'zxc'
    hashed_pass = hash_password(password)
    assert hashed_pass != password
    assert len(hashed_pass) > len(password)
    assert compare_password(password, hashed_password=hashed_pass)
    assert not compare_password('zxc123', hashed_password=hashed_pass)
