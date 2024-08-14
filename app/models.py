from app.database import Base
from sqlalchemy import String, text, ForeignKey
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column, relationship
from datetime import datetime


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] =  mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(String(255))
    published: Mapped[bool] = mapped_column(server_default='1')
    created_at: Mapped[datetime] = mapped_column(server_default=text('CURRENT_TIMESTAMP'))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="posts")


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=text('CURRENT_TIMESTAMP'))
    posts: Mapped[list["Posts"]] = relationship(back_populates="user")
