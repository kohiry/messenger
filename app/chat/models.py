from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Chat(Base):
    __tablename__ = "chat"

    id: Mapped[int] = mapped_column(primary_key=True)
    messages: Mapped[list["Message"]] = relationship(back_populates="Chat")
    first_user_id: Mapped[int] = mapped_column(Integer, nullable=False)
    second_user_id: Mapped[int] = mapped_column(Integer, nullable=False)


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    chat_id: Mapped[int] = mapped_column(ForeignKey('chat.id'))
    chat: Mapped["Chat"] = relationship(back_populates="messages")

    sender_id: Mapped[int] = mapped_column(Integer, nullable=False)
    recipient_id: Mapped[int] = mapped_column(Integer, nullable=False)

