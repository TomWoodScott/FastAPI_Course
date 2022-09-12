from optparse import Option
from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

@app.get('/blog')
def index(limit = 10, published: bool = True):
    # only get 10 published blogs
    if published:
        return {'data':f'{limit} published blogs'}
    else:
        return {'data': f'{limit} blogs from the db' }

@app.get('/blog/unpublished')
def unpublished():
    return {'data':'all unpublished blogs'}

@app.get('/blog/{id}')
def show(id: int):
    # fetch blog with id = id
    return {'data':id}

@app.get('/blog/{id}/comments')
def comments(id):
    # fetch comments of blocg with id = id
    return {'data':{'1', '2'}}

class Blog(BaseModel):
    title: str
    body: str
    published_at: Optional[bool] = False

@app.post('/blog')
def create_blog(request: Blog):
    return {'data': f"Blog is created with title: {request.title} and body :{request.body}"}

