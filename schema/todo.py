from pydantic import BaseModel, Field
from typing import Optional

class Todo(BaseModel):
    user_id: int 
    title: str = Field(..., min_length=1, max_length=255, description="Title must be between 1 and 255 characters")
    completed: bool = Field(False, description="Completion status of the todo")