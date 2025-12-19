from pydantic import BaseModel


class Debtor(BaseModel):
    full_name: str
    phone_number: str


class Debt(BaseModel):
    amount: int
    status: bool = False


class RequestPayment(BaseModel):
    amount: int

