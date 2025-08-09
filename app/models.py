from sqlalchemy import Column, Integer, Float, Enum
from sqlalchemy.orm import validates
from .db import Base
import enum

class LoanStatus(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    funded = "funded"
    closed = "closed"

class Loan(Base):
    __tablename__ = "loans"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    rate = Column(Float, nullable=False)
    term = Column(Integer, nullable=False)
    balance = Column(Float, nullable=False)
    status = Column(Enum(LoanStatus), default=LoanStatus.pending, nullable=False)

    @validates("amount", "rate", "term", "balance")
    def validate_non_negative(self, key, value):
        if value is None: 
            raise ValueError(f"{key} required")
        if key in ("amount","rate","balance") and value < 0:
            raise ValueError(f"{key} must be >= 0")
        if key == "term" and value <= 0:
            raise ValueError("term must be > 0")
        return value
