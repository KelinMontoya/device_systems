from sqlalchemy.orm import Session, joinedload
<<<<<<< HEAD
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
=======
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

>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
    db.commit()
    db.refresh(loan)
    return loan
