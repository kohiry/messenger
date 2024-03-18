from pydantic import BaseModel


class MessageSchema(BaseModel):
    id: int
    chat_id: int
    sender_id: int
    recipient_id: int
    text: str


class ChatSchema(BaseModel):
    id: int
    first_user_id: int
    second_user_id: int
    messages: list[MessageSchema] = []


class AnswerGood(BaseModel):
    status: int = 200
    message: str = "Done"

