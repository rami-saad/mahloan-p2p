from pydantic import BaseModel, Field
from typing import Literal

class LoanCreate(BaseModel):
    id: int
    amount: float = Field(ge=0)
    rate: float = Field(ge=0)
    term: int = Field(gt=0)
    balance: float = Field(ge=0)

class LoanOut(BaseModel):
    id: int
    amount: float
    rate: float
    term: int
    balance: float
    status: Literal["pending","approved","funded","closed"]
    class Config:
        from_attributes = True
