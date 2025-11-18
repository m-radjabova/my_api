from pydantic import BaseModel
from enum import Enum

class StatusType(str, Enum) :
    TODO = "TODO"
    INPROGRESS = "INPROGRESS"
    VERIFIED = "VERIFIED"
    DONE = "DONE"

class Status(BaseModel) :
    id : int
    title : StatusType
