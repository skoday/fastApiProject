from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
import mysql.connector


app = FastAPI()

config = {
    'user': 'root',
    'password': 'yoloxdrdz',
    'host': 'localhost',
    'database': 'fastapi'
}

try:
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
        cursor = connection.cursor(dictionary=True)

except mysql.connector.Error as err:
    print(f"Error: {err}")
"""finally: 
    if connection is not None and connection.is_connected():
        connection.close()
        print("MySQL connection is closed")"""


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: int | None = None


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/posts", status_code=status.HTTP_201_CREATED, tags=["posts"])
async def create_posts(post: Post):
    cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s)",
                   (post.title, post.content, post.published))
    connection.commit()
    # When we create a new post, we return the post created with the id.So we can use it later.
    return {"data": post}


@app.get("/posts", tags=["posts"])
async def get_posts():
    cursor.execute("SELECT * FROM posts")
    return {"data": cursor.fetchall()}


@app.get("/posts/{post_id}", tags=["posts"])
async def get_post(post_id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", [post_id])
    r = cursor.fetchone()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item not found",
                            headers={"X-Error": "There goes my error"})
    return {"data": r}


@app.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["posts"])
async def delete_post(post_id: int):
    cursor.execute("SELECT * FROM posts WHERE id = %s", [post_id])
    r = cursor.fetchone()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item not found",
                            headers={"X-Error": "There goes my error"})

    cursor.execute("DELETE FROM  posts WHERE id=%s", [post_id])
    cursor.fetchone()
    connection.commit()
    return


@app.put("/posts/{post_id}", tags=["posts"])
async def update_post(post_id: int, updated_post: Post):
    cursor.execute("SELECT * FROM posts WHERE id = %s", [post_id])
    r = cursor.fetchone()
    if not r:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Item not found",
                            headers={"X-Error": "There goes my error"})
    cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s",
                   [updated_post.title, updated_post.content, updated_post.published, post_id])
    cursor.fetchone()
    connection.commit()
    return
