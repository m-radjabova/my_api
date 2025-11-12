from pydantic import BaseModel

class Comment(BaseModel):
    postId: int
    name: str
    email: str
    body: str
