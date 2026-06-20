from fastapi import APIRouter, Query, Path, Depends
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services import loan_service
from app.dependencies.database_dependency import get_db

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get(
    "/",
    response_model=list[LoanResponse],
    summary="Listar préstamos",
    description="Retorna todos los préstamos. Permite filtrar por estado, usuario, dispositivo, email o tipo de dispositivo.",
)
def get_loans(
    db:          Session         = Depends(get_db),
    status:      Optional[str]   = Query(None, description="active | returned | overdue"),
    user_id:     Optional[int]   = Query(None),
    device_id:   Optional[int]   = Query(None),
    user_email:  Optional[str]   = Query(None),
    device_type: Optional[str]   = Query(None),
):
    return loan_service.get_all_loans(
        db, status=status, user_id=user_id, device_id=device_id,
        user_email=user_email, device_type=device_type
    )


@router.get(
    "/details",
    response_model=list[LoanDetailResponse],
    summary="Listar préstamos con información detallada (join)",
    description="Retorna los préstamos incluyendo datos del usuario y del dispositivo asociados (consulta con JOIN).",
)
def get_loans_details(
    db:          Session         = Depends(get_db),
    status:      Optional[str]   = Query(None),
    user_email:  Optional[str]   = Query(None),
    device_type: Optional[str]   = Query(None),
):
    return loan_service.get_all_loans(
        db, status=status, user_email=user_email, device_type=device_type
    )


@router.get(
    "/{loan_id}",
    response_model=LoanDetailResponse,
    summary="Obtener préstamo por ID (con datos relacionados)",
    responses={404: {"description": "Préstamo no encontrado"}},
)
def get_loan(
    loan_id: int     = Path(..., ge=1),
    db:      Session = Depends(get_db),
):
    return loan_service.get_loan_by_id(db, loan_id)


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=201,
    summary="Crear préstamo",
    description=(
        "Crea un nuevo préstamo. Valida que el usuario y el dispositivo existan "
        "y que el dispositivo esté disponible. Marca el dispositivo como no disponible."
    ),
    responses={
        404: {"description": "Usuario o dispositivo no encontrado"},
        409: {"description": "Dispositivo no disponible"},
    },
)
def create_loan(
    data: LoanCreate,
    db:   Session = Depends(get_db),
):
    return loan_service.create_loan(db, data)


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    summary="Devolver dispositivo",
    description="Marca el préstamo como devuelto, asigna fecha de devolución y libera el dispositivo.",
    responses={
        404: {"description": "Préstamo no encontrado"},
        409: {"description": "El préstamo ya fue devuelto"},
    },
)
def return_loan(
    loan_id: int     = Path(..., ge=1),
    db:      Session = Depends(get_db),
):
    return loan_service.return_loan(db, loan_id)
