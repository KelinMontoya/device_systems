from fastapi import APIRouter, Query, Response, Path, Depends, Request
from typing import Optional
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.services import user_service
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user, require_admin
from app.models.user_model import User

limiter = Limiter(key_func=get_remote_address)
router  = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserResponse], summary="Listar usuarios")
@limiter.limit("30/minute")
def get_users(
    request: Request,
    db: Session = Depends(get_db),
    role: Optional[str] = Query(None, enum=["admin", "support", "user"]),
    is_active: Optional[bool] = Query(None),
    order_by: Optional[str] = Query("id", enum=["id", "name", "created_at"]),
    _: User = Depends(get_current_active_user),
):
    return user_service.get_all_users(db, role=role, is_active=is_active, order_by=order_by)


@router.get("/{user_id}", response_model=UserResponse, summary="Obtener usuario por ID")
def get_user(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(get_current_active_user),
):
    return user_service.get_user_by_id(db, user_id)


@router.post("/", response_model=UserResponse, status_code=201, summary="Crear usuario")
def create_user(
    data: UserCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return user_service.create_user(db, data)


@router.put("/{user_id}", response_model=UserResponse, summary="Actualizar usuario completo")
def update_user(
    data: UserUpdate,
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return user_service.update_user(db, user_id, data)


@router.patch("/{user_id}", response_model=UserResponse, summary="Actualizar usuario parcial")
def patch_user(
    data: UserPatch,
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    return user_service.patch_user(db, user_id, data)


@router.delete("/{user_id}", status_code=204, summary="Eliminar usuario")
def delete_user(
    user_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    user_service.delete_user(db, user_id)
