from app.database import Base
from sqlalchemy import String, text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime


class Posts(Base):
    __tablename__ = "posts"

    id: Mapped[int] =  mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(100))
    content: Mapped[str] = mapped_column(String(255))
    published: Mapped[bool] = mapped_column(server_default='1')
    created_at: Mapped[datetime] = mapped_column(server_default=text('CURRENT_TIMESTAMP'))

    """id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    content = Column(String(255), nullable=False)
    published = Column(Boolean, server_default='1')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))"""


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(server_default=text('CURRENT_TIMESTAMP'))

    """
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    """