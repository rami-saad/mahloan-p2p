from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import Base, engine, SessionLocal
from .models import Loan
from .schemas import LoanCreate, LoanOut
from . import service
import time

Base.metadata.create_all(bind=engine)
app = FastAPI(title="Mahloan P2P")

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

@app.middleware("http")
async def timing_mw(request, call_next):
    start = time.time()
    resp = await call_next(request)
    resp.headers["X-Elapsed-ms"] = str(int((time.time()-start)*1000))
    return resp

@app.post("/loans", response_model=LoanOut)
def create(loan_in: LoanCreate, db: Session = Depends(get_db)):
    if service.get_loan(db, loan_in.id): raise HTTPException(400, "Loan exists")
    loan = Loan(**loan_in.model_dump())
    try: return service.create_loan(db, loan)
    except ValueError as e: raise HTTPException(400, str(e))

@app.post("/loans/{loan_id}/approve", response_model=LoanOut)
def approve(loan_id: int, db: Session = Depends(get_db)):
    loan = service.get_loan(db, loan_id)
    if not loan: raise HTTPException(404, "Not found")
    try: return service.approve(db, loan)
    except ValueError as e: raise HTTPException(400, str(e))

@app.post("/loans/{loan_id}/fund", response_model=LoanOut)
def fund(loan_id: int, db: Session = Depends(get_db)):
    loan = service.get_loan(db, loan_id)
    if not loan: raise HTTPException(404, "Not found")
    try: return service.fund(db, loan)
    except ValueError as e: raise HTTPException(400, str(e))

@app.post("/loans/{loan_id}/repay", response_model=LoanOut)
def repay(loan_id: int, amount: float, db: Session = Depends(get_db)):
    loan = service.get_loan(db, loan_id)
    if not loan: raise HTTPException(404, "Not found")
    try: return service.repay(db, loan, amount)
    except ValueError as e: raise HTTPException(400, str(e))

@app.get("/loans/{loan_id}", response_model=LoanOut)
def get(loan_id: int, db: Session = Depends(get_db)):
    loan = service.get_loan(db, loan_id)
    if not loan: raise HTTPException(404, "Not found")
    return loan

@app.get("/metrics")
def metrics():
    return {"status":"ok","version":"v1"}
