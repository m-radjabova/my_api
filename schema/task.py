from enum import Enum
from typing import List, Optional
from pydantic import BaseModel
from schema.status import  StatusType

class PriorityType(str, Enum):
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"

class Task(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    status: StatusType
    assignee: List[str]
    priority: List[PriorityType]
    end_date: str
    created_date: Optional[str] = None
