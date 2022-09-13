import re
from pydantic import BaseModel
from fastapi import FastAPI

app = FastAPI()

class Blog(BaseModel):
    title:str
    body:str

@app.post('/blog')
def create(request:Blog):
    return {'title':request.title, 'body':request.body}