from enum import Enum
from pydantic import BaseModel, EmailStr


class UserRole(str, Enum) :
    customer = "customer"
    provider = "provider"


class UserCreate(BaseModel) :
    name : str
    email : EmailStr
    password : str
    role :UserRole