from fastapi import APIRouter, Path, Depends, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetail
from app.services import loan_service
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin_or_support
from app.models.user_model import User

limiter = Limiter(key_func=get_remote_address)
router  = APIRouter(prefix="/loans", tags=["Loans"])


@router.get("/", response_model=list[LoanResponse], summary="Listar préstamos")
def get_loans(db: Session = Depends(get_db), _: User = Depends(get_current_active_user)):
    return loan_service.get_all_loans(db)


@router.get("/details", response_model=list[LoanDetail], summary="Préstamos con detalle")
def get_loan_details(db: Session = Depends(get_db), _: User = Depends(require_admin_or_support)):
    return loan_service.get_loans_with_details(db)


@router.post("/", response_model=LoanResponse, status_code=201, summary="Crear préstamo")
@limiter.limit("10/minute")
def create_loan(
    request: Request,
    data: LoanCreate,
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return loan_service.create_loan(db, data)


@router.patch("/{loan_id}/return", response_model=LoanResponse, summary="Registrar devolución")
def return_loan(
    loan_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_or_support),
):
    return loan_service.return_loan(db, loan_id)
