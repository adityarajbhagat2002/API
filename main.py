from fastapi import FastAPI
from fastapi.params import Body # it helps to import the body details from the http request we defined in the postman tool 
from typing import Optional
from pydantic import BaseModel # it helps us to create a schema such that what kind of data should the client(frontend) send to the backend



app=FastAPI()

class Post(BaseModel):
    title : str
    content: str
    published : bool=True
    rating :Optional[int] =None

@app.get("/")
async def root():
    return{"message" : "welcome to API !!! "}

@app.get("/posts")
async def get_post():
    return{"data" : "this is your data"}

@app.post("/createposts")
async def  create_posts(post : Post): # we are referncing the Post function class and storing it in a post variable
    
    print(post)
    print(post.dict())

    return {"data" : "New Post created"}


