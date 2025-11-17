from pydantic import BaseModel, EmailStr, Field

class User(BaseModel):
    id: int
    username: str = Field(..., min_length=5)
    email: EmailStr