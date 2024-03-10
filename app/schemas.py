from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, conint

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at : datetime


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    owner : UserOut
    

class Create_Post(BaseModel):
    title: str
    content: str
    published: bool = True

class Posts(Post):
    id: int


class User(BaseModel):
    email: EmailStr
    password : str



class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
    

class Vote(BaseModel):
    post_id : int
    dir: int
    

class PostOut(BaseModel):
    Post: Post
    votes: int

