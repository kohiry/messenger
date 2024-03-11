from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped

from app.database import Base


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    def to_dict(self):
        return {
            'username': self.username,
            'id': self.id,
            'email': self.email,
        }
