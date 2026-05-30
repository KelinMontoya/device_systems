from fastapi import APIRouter, Query, Response, Path, Depends
from typing import Optional

from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.services import user_service
from app.dependencies.user_dependencies import get_user_or_404, get_api_config, verify_api_key

router = APIRouter(prefix="/users", tags=["Users"])


def set_headers(response: Response):
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "2.0"


# ── GET /users ────────────────────────────────────────────────────────────────
@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Filtra por rol y/o estado.",
    response_description="Lista de usuarios",
)
def get_users(
    response: Response,
    role:      Optional[str]  = Query(None, enum=["admin", "support", "user"]),
    is_active: Optional[bool] = Query(None),
):
    set_headers(response)
    return user_service.get_all_users(role=role, is_active=is_active)


# ── GET /users/{user_id} ──────────────────────────────────────────────────────
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Busca un usuario específico por su ID.",
)
def get_user(
    response: Response,
    user: dict = Depends(get_user_or_404),
):
    set_headers(response)
    return user


# ── POST /users ───────────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario",
    description="Registra un nuevo usuario. Evita correos duplicados.",
)
def create_user(data: UserCreate, response: Response):
    set_headers(response)
    return user_service.create_user(data)


# ── PUT /users/{user_id} ──────────────────────────────────────────────────────
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario completo",
    description="Reemplaza TODOS los campos del usuario.",
)
def update_user(
    data:     UserUpdate,
    response: Response,
    user_id:  int  = Path(..., ge=1),
    _user:    dict = Depends(get_user_or_404),   # valida que exista
):
    set_headers(response)
    return user_service.update_user(user_id, data)


# ── PATCH /users/{user_id} ────────────────────────────────────────────────────
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Actualizar usuario parcial",
    description="Modifica solo los campos enviados. Mínimo 1 campo requerido.",
)
def patch_user(
    data:     UserPatch,
    response: Response,
    user_id:  int  = Path(..., ge=1),
    _user:    dict = Depends(get_user_or_404),
):
    set_headers(response)
    return user_service.patch_user(user_id, data)


# ── DELETE /users/{user_id} ───────────────────────────────────────────────────
@router.delete(
    "/{user_id}",
    status_code=204,
    summary="Eliminar usuario",
    description="Elimina un usuario por ID. Retorna 204 sin contenido.",
)
def delete_user(
    user_id: int  = Path(..., ge=1),
    _user:   dict = Depends(get_user_or_404),
):
    user_service.delete_user(user_id)