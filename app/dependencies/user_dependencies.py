from fastapi import Depends, HTTPException, Header
from app.data.users_db import users_db
from app.schemas.user_schema import RoleEnum


# ── Dependencia: obtener usuario o lanzar 404 ─────────────────────────────────
def get_user_or_404(user_id: int) -> dict:
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con id={user_id} no encontrado"
        )
    return user


# ── Dependencia: verificar si email ya existe ─────────────────────────────────
def check_email_unique(email: str) -> str:
    if any(u["email"] == email for u in users_db):
        raise HTTPException(
            status_code=400,
            detail=f"El correo '{email}' ya está registrado"
        )
    return email


# ── Dependencia: configuración general de la API ──────────────────────────────
def get_api_config() -> dict:
    return {
        "app_name": "device_systems",
        "version":  "2.0.0",
        "author":   "SENA"
    }


# ── Dependencia: autenticación básica por cabecera ────────────────────────────
def verify_api_key(x_api_key: str = Header(default=None)) -> str:
    API_KEY = "device2024"
    if x_api_key != API_KEY:
        raise HTTPException(
            status_code=401,
            detail="API Key inválida o no proporcionada. Usa el header: X-API-Key: device2024"
        )
    return x_api_key