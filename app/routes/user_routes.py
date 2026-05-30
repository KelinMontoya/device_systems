from fastapi import APIRouter, HTTPException, Query, Response, Path
from typing import Optional

from app.schemas.user_schema import UserCreate, UserResponse, UserListResponse

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

# ── Simulated in-memory DB ────────────────────────────────────────────────────
users_db: list[dict] = [
    {"id": 1, "name": "Ana Torres",    "email": "ana@mail.com",    "role": "admin",   "is_active": True},
    {"id": 2, "name": "Luis Gomez",    "email": "luis@mail.com",   "role": "support", "is_active": True},
    {"id": 3, "name": "Maria Ruiz",    "email": "maria@mail.com",  "role": "user",    "is_active": False},
    {"id": 4, "name": "Pedro Silva",   "email": "pedro@mail.com",  "role": "user",    "is_active": True},
]
_id_counter = {"value": 5}


# ── Helper: cabeceras personalizadas ─────────────────────────────────────────
def set_custom_headers(response: Response) -> None:
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "1.0"


# ─────────────────────────────────────────────────────────────────────────────
# GET /users  — lista completa con filtros opcionales
# ─────────────────────────────────────────────────────────────────────────────
@router.get(
    "/",
    response_model=UserListResponse,
    summary="Listar usuarios",
    description="Retorna todos los usuarios. Permite filtrar por rol y/o estado activo.",
)
def get_users(
    response: Response,
    role: Optional[str] = Query(
        default=None,
        description="Filtrar por rol: admin | support | user",
        enum=["admin", "support", "user"],
    ),
    is_active: Optional[bool] = Query(
        default=None,
        description="Filtrar por estado: true | false",
    ),
):
    set_custom_headers(response)
    result = list(users_db)

    if role is not None:
        result = [u for u in result if u["role"] == role]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]

    return {"total": len(result), "users": result}


# ─────────────────────────────────────────────────────────────────────────────
# GET /users/{user_id}  — buscar por ID (Path Parameter)
# ─────────────────────────────────────────────────────────────────────────────
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Obtener usuario por ID",
    description="Busca y retorna un usuario específico por su ID.",
)
def get_user_by_id(
    response: Response,
    user_id: int = Path(..., ge=1, description="ID del usuario (entero positivo)"),
):
    set_custom_headers(response)
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con id={user_id} no encontrado",
        )
    return user


# ─────────────────────────────────────────────────────────────────────────────
# POST /users  — crear usuario
# ─────────────────────────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=UserResponse,
    status_code=201,
    summary="Crear usuario",
    description="Registra un nuevo usuario. Valida datos con Pydantic y evita correos duplicados.",
)
def create_user(user_data: UserCreate, response: Response):
    set_custom_headers(response)

    # Verificar email duplicado
    if any(u["email"] == user_data.email for u in users_db):
        raise HTTPException(
            status_code=400,
            detail=f"El correo '{user_data.email}' ya está registrado",
        )

    new_user = {
        "id": _id_counter["value"],
        **user_data.model_dump(),
    }
    _id_counter["value"] += 1
    users_db.append(new_user)

    return new_user