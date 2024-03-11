from pydantic import BaseModel


class UserIn(BaseModel):
    email: str
    username: str
    password: str


class UserOut(BaseModel):
    username: str
    id: int
    email: str


class CreatedUserMessage(BaseModel):
    result: str = "User Created"
