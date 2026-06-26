from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.schemas.auth_schema import UserRegister, Token
from app.schemas.user_schema import UserResponse
from app.auth import auth_service
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user
from app.models.user_model import User

limiter = Limiter(key_func=get_remote_address)
router  = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=201,
    summary="Registrar nuevo usuario",
    description="Crea un usuario con contraseña hasheada. Valida seguridad de contraseña.",
    responses={400: {"description": "Email duplicado"}, 422: {"description": "Contraseña débil o datos inválidos"}},
)
@limiter.limit("3/minute")
def register(request: Request, data: UserRegister, db: Session = Depends(get_db)):
    return auth_service.register_user(db, data)


@router.post(
    "/login",
    response_model=Token,
    summary="Iniciar sesión",
    description="Autentica al usuario con email/password y retorna un token JWT Bearer.",
    responses={401: {"description": "Credenciales incorrectas"}},
)
@limiter.limit("5/minute")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user  = auth_service.authenticate_user(db, form_data.username, form_data.password)
    return auth_service.generate_token(user)


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Datos del usuario autenticado",
    description="Retorna los datos del usuario autenticado. No expone hashed_password.",
)
def me(current_user: User = Depends(get_current_active_user)):
    return current_user
