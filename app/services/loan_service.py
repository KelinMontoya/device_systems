from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from datetime import datetime, timezone

from app.models.loan_model import Loan
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate


def get_all_loans(db: Session):
    return db.query(Loan).all()


def get_loan_by_id(db: Session, loan_id: int) -> Loan:
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail=f"Préstamo id={loan_id} no encontrado")
    return loan


def get_loans_with_details(db: Session):
    loans = db.query(Loan).options(joinedload(Loan.user), joinedload(Loan.device)).all()
    result = []
    for loan in loans:
        result.append({
            "id": loan.id,
            "loan_date": loan.loan_date,
            "return_date": loan.return_date,
            "is_returned": loan.is_returned,
            "notes": loan.notes,
            "user_name": loan.user.name,
            "user_email": loan.user.email,
            "device_name": loan.device.name,
            "device_serial": loan.device.serial,
            "device_brand": loan.device.brand,
        })
    return result


def create_loan(db: Session, data: LoanCreate) -> Loan:
    device = db.query(Device).filter(Device.id == data.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    if not device.is_available:
        raise HTTPException(status_code=400, detail="El dispositivo no está disponible")

    loan = Loan(
        user_id=data.user_id,
        device_id=data.device_id,
        notes=data.notes,
    )
    device.is_available = False
    db.add(loan)
    db.commit()
    db.refresh(loan)
    return loan


def return_loan(db: Session, loan_id: int) -> Loan:
    loan = get_loan_by_id(db, loan_id)
    if loan.is_returned:
        raise HTTPException(status_code=400, detail="El préstamo ya fue devuelto")
    loan.is_returned = True
    loan.return_date = datetime.now(timezone.utc)
    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True
    db.commit()
    db.refresh(loan)
    return loan
