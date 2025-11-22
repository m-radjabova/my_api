
from typing import List
from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: int
    username: str
    email: EmailStr

class RequestUser(BaseModel):
    username: str = Field(..., min_length=5)
    email: EmailStr

class Team(BaseModel):
    id: int
    name: str
    members: List[User]

class RequestTeam(BaseModel):
    name: str