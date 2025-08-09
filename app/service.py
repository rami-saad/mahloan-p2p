from sqlalchemy.orm import Session
from .models import Loan, LoanStatus
from typing import Optional

def create_loan(db: Session, loan: Loan) -> Loan:
    db.add(loan); db.commit(); db.refresh(loan); return loan

def get_loan(db: Session, loan_id: int) -> Optional[Loan]:
    return db.query(Loan).filter(Loan.id == loan_id).first()

def approve(db: Session, loan: Loan) -> Loan:
    if loan.status != LoanStatus.pending: raise ValueError("Only pending loans can be approved")
    loan.status = LoanStatus.approved; db.commit(); db.refresh(loan); return loan

def fund(db: Session, loan: Loan) -> Loan:
    if loan.status != LoanStatus.approved: raise ValueError("Only approved loans can be funded")
    loan.status = LoanStatus.funded; db.commit(); db.refresh(loan); return loan

def repay(db: Session, loan: Loan, amount: float) -> Loan:
    if amount <= 0: raise ValueError("Repayment must be > 0")
    loan.balance = max(0.0, loan.balance - amount)
    if loan.balance == 0 and loan.status == LoanStatus.funded: loan.status = LoanStatus.closed
    db.commit(); db.refresh(loan); return loan
