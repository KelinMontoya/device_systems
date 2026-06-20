from fastapi import APIRouter, Query, Response, Path, Depends
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.schemas.loan_schema import LoanDetailResponse
from app.services import user_service, loan_service
from app.dependencies.database_dependency import get_db

router = APIRouter(prefix="/users", tags=["Users"])


def set_headers(response: Response):
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "3.0"


# ── GET /users ────────────────────────────────────────────────────────────────
@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Filtra por rol, estado y ordena por campo.",
    response_description="Lista de usuarios",
)
def get_users(
    response:  Response,
    db:        Session = Depends(get_db),
    role:      Optional[str]  = Query(None, enum=["admin", "support", "user"]),
    is_active: Optional[bool] = Query(None),
    order_by:  Optional[str]  = Query("id", enum=["id", "name", "created_at"]),
):
    set_headers(response)
    return user_service.get_all_users(db, role=role, is_active=is_active, order_by=order_by)


# ── GET /users/{user_id} ──────────────────────────────────────────────────────
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Busca un usuario específico por su ID.",
    responses={404: {"description": "Usuario no encontrado"}},
)
def get_user(
    response: Response,
    user_id:  int     = Path(..., ge=1),
    db:       Session = Depends(get_db),
):
    set_headers(response)
    return user_service.get_user_by_id(db, user_id)


# ── POST /users ───────────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario",
    description="Registra un nuevo usuario en la base de datos. El correo debe ser único.",
    responses={400: {"description": "Email duplicado"}},
)
def create_user(
    data:     UserCreate,
    response: Response,
    db:       Session = Depends(get_db),
):
    set_headers(response)
    return user_service.create_user(db, data)


# ── PUT /users/{user_id} ──────────────────────────────────────────────────────
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo",
    description="Reemplaza TODOS los campos del usuario.",
    responses={404: {"description": "Usuario no encontrado"}, 400: {"description": "Email duplicado"}},
)
def update_user(
    data:     UserUpdate,
    response: Response,
    user_id:  int     = Path(..., ge=1),
    db:       Session = Depends(get_db),
):
    set_headers(response)
    return user_service.update_user(db, user_id, data)


# ── PATCH /users/{user_id} ────────────────────────────────────────────────────
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcial",
    description="Modifica solo los campos enviados. Mínimo 1 campo requerido.",
    responses={404: {"description": "Usuario no encontrado"}},
)
def patch_user(
    data:     UserPatch,
    response: Response,
    user_id:  int     = Path(..., ge=1),
    db:       Session = Depends(get_db),
):
    set_headers(response)
    return user_service.patch_user(db, user_id, data)


# ── DELETE /users/{user_id} ───────────────────────────────────────────────────
@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Eliminar usuario",
    description="Elimina un usuario por ID. Retorna 204 sin contenido.",
    responses={404: {"description": "Usuario no encontrado"}},
)
def delete_user(
    user_id: int     = Path(..., ge=1),
    db:      Session = Depends(get_db),
):
    user_service.delete_user(db, user_id)


# ── GET /users/{user_id}/loans ────────────────────────────────────────────────
@router.get(
    "/{user_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Préstamos de un usuario",
    description="Retorna todos los préstamos asociados a un usuario, incluyendo datos del dispositivo (JOIN).",
    responses={404: {"description": "Usuario no encontrado"}},
)
def get_user_loans(
    user_id: int     = Path(..., ge=1),
    db:      Session = Depends(get_db),
):
    return loan_service.get_loans_by_user(db, user_id)
