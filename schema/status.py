from pydantic import BaseModel

class Status(BaseModel) :
    id : int
    title : str
