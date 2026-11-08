from enum import Enum
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserRole(str, Enum) :
    customer = "customer"
    provider = "provider"


class UserCreate(BaseModel) :
    name : str
    email : EmailStr
    password : str
    role :UserRole


class UserOut(BaseModel) :
    id : int
    email : EmailStr
    created_at : datetime

    class Config :
        orm_model = True


class UserLogin(BaseModel) :
    email : EmailStr
    password : str


class Token(BaseModel) :
    access_token : str
    token_type : str


class TokenData(BaseModel) :
    id : Optional[int] = None