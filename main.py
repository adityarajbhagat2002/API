from fastapi import FastAPI
from fastapi.params import Body # it helps to import the body details from the http request we defined in the postman tool 
from typing import Optional
from pydantic import BaseModel # it helps us to create a schema such that what kind of data should the client(frontend) send to the backend
from random import randrange


app=FastAPI()

class Post(BaseModel):
    title : str
    content: str
    published : bool=True
    rating :Optional[int] =None

my_post=[{"title": "title of the post 1" , "content" : "content of the post 1","id" : 1},
{"title" : "favourite food", "content":"I like pizza" , "id" : 2}]

@app.get("/")
async def root():
    return{"message" : "welcome to API !!! "}

@app.get("/posts")
async def get_post():
    return{"data" : my_post}

@app.post("/posts")
async def  create_posts(post : Post): # we are referncing the Post function class and storing it in a post variable
    post_dict= post.dict()
    post_dict['id'] = randrange(0,10000000)
    my_post.append(post_dict)

    return {"data" : post_dict}


