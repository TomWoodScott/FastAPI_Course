from re import T
from tokenize import String
from pydantic import BaseModel

# blog schema
class Blog(BaseModel):
    title:str
    body:str


# schema more specific endpoints
class ShowBlog(BaseModel):
    title: str
    body: str
    class Config():
        orm_mode=True

class User(BaseModel):
    name: str
    email: str
    password: str