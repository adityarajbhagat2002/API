import sys
from fastapi import FastAPI, Response, status, HTTPException, Depends
# it helps to import the body details from the http request we defined in the postman tool
from fastapi.params import Body
from typing import Optional
# it helps us to create a schema such that what kind of data should the client(frontend) send to the backend
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session

from database import engine, get_db
import models
app = FastAPI()

models.Base.metadata.create_all(bind=engine)


class Post(BaseModel):  # to define the schema for the client
    title: str
    content: str
    published: bool = True


while True:

    try:

        conn = psycopg2.connect(host="localhost", database="fastapi", user="postgres", password="aditya900",
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was sucessfully established !!")
        break
    except Exception as error:
        print("Connection to database failed")
        print("Error : ", error)
        time.sleep(2)


my_post = [{"title": "title of the post 1", "content": "content of the post 1", "id": 1},
           {"title": "favourite food", "content": "I like pizza", "id": 2}]


def find_post(id):
    for p in my_post:
        if p["id"] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i


@app.get("/")
async def root():
    return {"message": "welcome to API !!! "}


@app.get("/sqlalchemy")
def test_post(db: Session = Depends(get_db)):
    return {"status": "Sucessfull"}


@app.get("/posts")
async def get_post():
    cursor.execute(""" SELECT * FROM posts """)
    posts = cursor.fetchall()
    return {"data": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
# we are referncing the Post function class and storing it in a post variable
async def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title , content , published) VALUES (%s, %s , %s )RETURNING *
    """, (post.title, post.content, post.published))
    new_post = cursor.fetchall()
    conn.commit()

    return {"data": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with this id {id} was not found ")

    return {"post_details": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """ DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} is not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    cursor.execute(""" UPDATE posts SET title=%s  , content =%s ,published = %s  WHERE id = %s RETURNING * """,
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id {id} is not found")

    return {"data": updated_post}
