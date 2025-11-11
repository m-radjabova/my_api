from pydantic import BaseModel, Field
from typing import Optional

class Post(BaseModel):
    title: str = Field(..., min_length=5, max_length=100, description="Title must be between 5 and 100 characters")
    body: Optional[str] = None
    user_id: int
