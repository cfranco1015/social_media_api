from lib2to3.pytree import Base
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime
# create a Pydantic model to validate data being sent from server
# each field can have an assigned a data type, a default value or to none

class UserCreate(BaseModel):
    email : EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True    

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id : int
    created_at: datetime
    owner_id: int
    owner: UserOut

    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post:  Post
    votes: int

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

# Caution: conint can cause negative values
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)

