from fastapi import HTTPException, status, Depends, APIRouter
from app.database import get_db
from sqlalchemy.orm import Session
from app import models
from sqlalchemy import literal, select, update
from app import schemas, oauth2
from typing import Any

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
async def create_post(post: schemas.PostBase, db: Session = Depends(get_db),
                      current_user: models.Users = Depends(oauth2.get_current_user)) -> Any:
    new_post = models.Posts(user_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=list[schemas.PostResponse])
async def get_posts(db: Session = Depends(get_db),
                    current_user: models.Users = Depends(oauth2.get_current_user)):
    posts = db.execute(select(models.Posts)).scalars().all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no posts available")
    return posts


@router.get("/me", response_model=list[schemas.PostResponse])
async def my_posts(current_user: models.Users = Depends(oauth2.get_current_user),
                   db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str | None = "") -> Any:

    posts = db.execute(
                        select(models.Posts).where(models.Posts.user_id == current_user.id)
                        .where(models.Posts.title.contains(search))
                        .offset(skip).limit(limit)
                       ).scalars().all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There are no posts available")
    print(posts)
    return posts


@router.get("/{post_id}", response_model=schemas.PostResponse)
async def get_post(post_id: int, db: Session = Depends(get_db),
                   current_user: models.Users = Depends(oauth2.get_current_user)) -> Any:
    r = db.get(models.Posts, post_id)
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,  detail="Item not found")
    if r.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to be here")
    return r


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(post_id: int, db: Session = Depends(get_db),
                      current_user: models.Users = Depends(oauth2.get_current_user)):
    r = db.get(models.Posts, post_id)
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    if r.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to delete this post")

    db.delete(r)
    db.commit()
    return


@router.put("/{post_id}", response_model=schemas.PostResponse)
async def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                      current_user: models.Users = Depends(oauth2.get_current_user)) -> Any:
    post = db.get(models.Posts, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    if post.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not allowed to modify this post")

    db.execute(update(models.Posts).where(models.Posts.id == literal(post_id)).values(**updated_post.model_dump()))
    db.commit()
    return post
