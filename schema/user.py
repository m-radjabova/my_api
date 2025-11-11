from pydantic import BaseModel, EmailStr, Field, StringConstraints
from typing import Annotated

class User(BaseModel):
    username: str = Field(..., min_length=5)
    email: EmailStr
    phone_number: Annotated[str, StringConstraints(pattern=r"^\+998\d{9}$")]
    age: int = Field(...,gt=18,le=100,description="age must be 18 ")
    address: str
