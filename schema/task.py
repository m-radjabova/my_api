from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

from schema.user import User

class StatusType(str, Enum):
    TODO = "TODO"
    INPROGRESS = "IN_PROGRESS"
    VERIFIED = "VERIFIED"
    DONE = "DONE"

class Task(BaseModel):
    id: int
    title: str
    description: str
    status: StatusType
    assignees: List[User]
    priority: str
    end_date: str
    created_date: Optional[str] = None

class ResponseTask(BaseModel):
    status: StatusType
    tasks: List[Task]

class RequestTask(BaseModel):
    title: str
    description: str
    status: StatusType
    assignees: List[User]
    priority: str
    end_date: str
