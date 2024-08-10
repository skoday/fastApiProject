from fastapi import FastAPI, HTTPException, status, Depends
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app import models
from sqlalchemy import literal, select, update
from app import schemas, utils


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse, tags=["posts"])
async def create_posts(post: schemas.PostBase, db: Session = Depends(get_db)):
    new_post = models.Posts(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts", tags=["posts"])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.execute(select(models.Posts)).scalars().all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="There are no posts available",
                            headers={"X-Error": "There goes my error"})
    return posts


@app.get("/posts/{post_id}", response_model=schemas.PostResponse, tags=["posts"])
async def get_post(post_id: int, db: Session = Depends(get_db)):
    r = db.get(models.Posts, post_id)
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item not found",
                            headers={"X-Error": "There goes my error"})
    return r


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["posts"])
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    r = db.get(models.Posts, post_id)
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item not found",
                            headers={"X-Error": "There goes my error"})
    db.delete(r)
    db.commit()
    return


@app.put("/posts/{post_id}", response_model=schemas.PostResponse, tags=["posts"])
async def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = db.get(models.Posts, post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item not found",
                            headers={"X-Error": "There goes my error"})
    db.execute(update(models.Posts).where(models.Posts.id == literal(post_id)).values(**updated_post.model_dump()))
    db.commit()
    return post


# Users
@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut, tags=["users"])
async def create_user(user: schemas.CreateUser, db: Session = Depends(get_db)):
    # hash the password
    user.password = utils.hash_password(user.password)

    new_user = models.Users(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
