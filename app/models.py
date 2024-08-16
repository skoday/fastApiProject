from app.database import Base
from sqlalchemy import String, text, ForeignKey
from sqlalchemy.orm import Mapped, relationship
from sqlalchemy.orm import mapped_column
from datetime import datetime


"""
    As we are creating a kind of social interaction where a user can retireve all its posts and
    each post has the user's info the a bidirectional relationship is created between the two tables.
    Plus each post need to have a user_id to know which user created the post so on delete cascade is
    added to the foreign key.
"""


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(String(255))
    published: Mapped[bool] = mapped_column(server_default='1')
    created_at: Mapped[datetime] = mapped_column(server_default=text('CURRENT_TIMESTAMP'))
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    user: Mapped["Users"] = relationship(back_populates="posts")


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=text('CURRENT_TIMESTAMP'))
    posts: Mapped[list["Posts"]] = relationship(back_populates="user", cascade="all, delete")
