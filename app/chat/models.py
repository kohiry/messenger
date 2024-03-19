from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.user.models import User


class Message(Base):
    __tablename__ = "message"

    id: Mapped[int] = mapped_column(primary_key=True)
    sender_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    sender: Mapped["User"] = relationship("User", back_populates="sent")
    receiver_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"), nullable=False)
    receiver: Mapped["User"] = relationship("User", back_populates="received")
    text: Mapped[str] = mapped_column(String(255), nullable=True)
    attachment: Mapped[str] = mapped_column(String(255), nullable=True)

    def get_dict(self):
        return {
            "id": self.id,
            "sender": self.sender.to_dict(),
            "receiver": self.receiver.to_dict(),
            "text": self.text,
            "attachment": self.attachment
        }
