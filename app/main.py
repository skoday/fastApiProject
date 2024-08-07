from fastapi import FastAPI, HTTPException, status, Depends
from app.database import engine, get_db
from sqlalchemy.orm import Session
from app import models
from sqlalchemy import literal
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


@app.get("/posts", response_model=list[schemas.PostResponse], tags=["posts"])
async def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Posts).all()
    return posts


@app.get("/posts/{post_id}", response_model=schemas.PostResponse, tags=["posts"])
async def get_post(post_id: int, db: Session = Depends(get_db)):
    r = db.query(models.Posts).filter(models.Posts.id == literal(post_id)).first()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item not found",
                            headers={"X-Error": "There goes my error"})
    return r


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["posts"])
async def delete_post(post_id: int, db: Session = Depends(get_db)):
    r = db.query(models.Posts).filter(models.Posts.id == literal(post_id))
    if not r.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item not found",
                            headers={"X-Error": "There goes my error"})
    r.delete(synchronize_session=False)
    db.commit()
    return


@app.put("/posts/{post_id}", response_model=schemas.PostResponse, tags=["posts"])
async def update_post(post_id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):
    post = db.query(models.Posts).filter(models.Posts.id == literal(post_id))
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item not found",
                            headers={"X-Error": "There goes my error"})
    post.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()
    return post.first()


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
