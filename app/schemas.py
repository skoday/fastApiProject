from pydantic import BaseModel, EmailStr
from datetime import datetime
from app import votes_enum


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class CreateUser(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime


class PostResponse(PostBase):
    id: int
    created_at: datetime
    # user_id: int
    user: UserOut


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int | None = None


class Vote(BaseModel):
    dir: votes_enum.VoteDirection


class CreateVote(Vote):
    post_id: int
