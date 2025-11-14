from pydantic import BaseModel, EmailStr, Field, StringConstraints
from typing import Annotated, Dict

class User(BaseModel):
    id: int
    username: str = Field(..., min_length=5)
    email: EmailStr
    address: Dict[str, str]