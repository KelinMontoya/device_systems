from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from fastapi import HTTPException
from datetime import datetime

from app.models.loan_model import Loan
from app.models.device_model import Device
from app.models.user_model import User
from app.schemas.loan_schema import LoanCreate


# ── Listar préstamos con joins y filtros avanzados ────────────────────────────
def get_all_loans(
    db: Session,
    status: str = None,
    user_id: int = None,
    device_id: int = None,
    user_email: str = None,
    device_type: str = None,
) -> list[Loan]:
    query = (
        db.query(Loan)
        .join(User, Loan.user_id == User.id)
        .join(Device, Loan.device_id == Device.id)
        .options(joinedload(Loan.user), joinedload(Loan.device))
    )

    filters = []
    if status is not None:
        filters.append(Loan.status == status)
    if user_id is not None:
        filters.append(Loan.user_id == user_id)
    if device_id is not None:
        filters.append(Loan.device_id == device_id)
    if user_email is not None:
        filters.append(User.email.ilike(f"%{user_email}%"))
    if device_type is not None:
        filters.append(Device.device_type == device_type)

    if filters:
        query = query.filter(and_(*filters))

    return query.order_by(Loan.id).all()


def get_loan_by_id(db: Session, loan_id: int) -> Loan:
    loan = (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.id == loan_id)
        .first()
    )
    if not loan:
        raise HTTPException(
            status_code=404,
            detail=f"Préstamo con id={loan_id} no encontrado"
        )
    return loan


def get_loans_by_user(db: Session, user_id: int) -> list[Loan]:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con id={user_id} no encontrado")

    return (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.user_id == user_id)
        .order_by(Loan.id)
        .all()
    )


def get_loans_by_device(db: Session, device_id: int) -> list[Loan]:
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Dispositivo con id={device_id} no encontrado")

    return (
        db.query(Loan)
        .options(joinedload(Loan.user), joinedload(Loan.device))
        .filter(Loan.device_id == device_id)
        .order_by(Loan.id)
        .all()
    )


# ── Crear préstamo (valida usuario, dispositivo y disponibilidad) ────────────
def create_loan(db: Session, data: LoanCreate) -> Loan:
    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con id={data.user_id} no encontrado")

    device = db.query(Device).filter(Device.id == data.device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Dispositivo con id={data.device_id} no encontrado")

    if not device.is_available:
        raise HTTPException(
            status_code=409,
            detail=f"El dispositivo '{device.name}' no está disponible para préstamo"
        )

    new_loan = Loan(
        user_id=data.user_id,
        device_id=data.device_id,
        loan_date=datetime.utcnow(),
        status="active",
    )
    device.is_available = False

    db.add(new_loan)
    db.commit()
    db.refresh(new_loan)
    return new_loan


# ── Devolver dispositivo ───────────────────────────────────────────────────────
def return_loan(db: Session, loan_id: int) -> Loan:
    loan = db.query(Loan).filter(Loan.id == loan_id).first()
    if not loan:
        raise HTTPException(status_code=404, detail=f"Préstamo con id={loan_id} no encontrado")

    if loan.status == "returned":
        raise HTTPException(
            status_code=409,
            detail="Este préstamo ya fue devuelto anteriormente"
        )

    loan.status      = "returned"
    loan.return_date = datetime.utcnow()

    device = db.query(Device).filter(Device.id == loan.device_id).first()
    if device:
        device.is_available = True

    db.commit()
    db.refresh(loan)
    return loan
