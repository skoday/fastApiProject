from fastapi import HTTPException, status, Depends, APIRouter
from app.database import get_db
from sqlalchemy.orm import Session
from app import models
from sqlalchemy import literal, select, update
from app import schemas, oauth2
from typing import Any


router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Vote)
async def vote(vote: schemas.CreateVote, db: Session = Depends(get_db),
               current_user: models.Users = Depends(oauth2.get_current_user)) -> Any:
    post = db.get(models.Posts, vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    if vote.dir == 1:
        if current_user in post.likes:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already liked this post")
        else:
            post.likes.append(current_user)
            db.commit()
    else:
        if current_user in post.likes:
            post.likes.remove(current_user)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User has not liked this post")
    return vote
