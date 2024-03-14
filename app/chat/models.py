from typing import List

from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(primary_key=True)
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="chat")
    first_user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    second_user_id: Mapped[int] = mapped_column(Integer, nullable=False)

    def get_dict(self):
        return {
            "id": self.id,
            "first_user_id": self.first_user_id,
            "second_user_id": self.second_user_id,
        }


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(Integer, ForeignKey('chat.id'))
    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")

    sender_id: Mapped[int] = mapped_column(Integer, nullable=False)
    recipient_id: Mapped[int] = mapped_column(Integer, nullable=False)
    text: Mapped[str] = mapped_column(String(255), nullable=False)

    def get_dict(self):
        return {
            "id": self.id,
            "chat_id": self.chat_id,
            "sender_id": self.sender_id,
            "recipient_id": self.recipient_id,
            "text": self.text,
        }

