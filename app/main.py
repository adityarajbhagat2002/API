from fastapi import FastAPI,Response,status,HTTPException   
from fastapi.params import Body  # it helps to import the body details from the http request we defined in the postman tool 
from typing import Optional
from pydantic import BaseModel # it helps us to create a schema such that what kind of data should the client(frontend) send to the backend
from random import randrange


app=FastAPI()

class Post(BaseModel):#to define the schema for the client 
    title : str
    content: str
    published : bool=True
    rating :Optional[int] =None

my_post=[{"title": "title of the post 1" , "content" : "content of the post 1","id" : 1},
{"title" : "favourite food", "content":"I like pizza" , "id" : 2}]


def find_post(id):
    for p in my_post : 
        if p["id"]== id:
            return p 


def find_index_post(id):
    for i, p in enumerate(my_post):
        if p["id"]== id:
            return i

@app.get("/")
async def root():
    return{"message" : "welcome to API !!! "}

@app.get("/posts")
async def get_post():
    return{"data" : my_post}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
async def  create_posts(post : Post): # we are referncing the Post function class and storing it in a post variable
    post_dict= post.dict()
    post_dict['id'] = randrange(0,10000000)
    my_post.append(post_dict) 

    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id:int , response : Response):
    post=find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with this id {id} was not found ")
    
    return{"post_details" : post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    index=find_index_post(id)
    if index==None:
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} is not found")
    
    my_post.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post: Post):
   
    index=find_index_post(id)
    if index==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
        detail=f"post with id {id} is not found")
    
    post_dict=post.dict()
    post_dict['id']=id          
    my_post[index]=post_dict
    return {"data" : post_dict}








