from fastapi import FastAPI
from fastapi.params import Body


app=FastAPI()

@app.get("/")
async def root():
    return{"message" : "welcome to API !!! "}

@app.get("/posts")
async def get_post():
    return{"data" : "this is your data"}

@app.post("/createposts")
async def  create_posts(payload :dict = Body(...)):
    print(payload)
    return {"new_post": f"title {payload['title']} ,content {payload['title']}"}
    