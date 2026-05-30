from pydantic import BaseModel, EmailStr, field_validator, Field
from typing import Optional
from enum import Enum


# ── Enum de roles permitidos ──────────────────────────────────────────────────
class RoleEnum(str, Enum):
    admin   = "admin"
    support = "support"
    user    = "user"


# ── Modelo de ENTRADA (lo que recibe el POST) ─────────────────────────────────
class UserCreate(BaseModel):
    name:      str       = Field(..., min_length=3, description="Nombre completo, mínimo 3 caracteres")
    email:     EmailStr  = Field(..., description="Correo electrónico válido")
    role:      RoleEnum  = Field(..., description="Rol: admin | support | user")
    is_active: bool      = Field(default=True, description="Estado activo/inactivo")

    @field_validator("name")
    @classmethod
    def name_no_spaces_only(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("El nombre no puede estar vacío o contener solo espacios")
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Carlos Perez",
                    "email": "carlos@email.com",
                    "role": "admin",
                    "is_active": True
                }
            ]
        }
    }


# ── Modelo de RESPUESTA (lo que devuelve la API) ──────────────────────────────
class UserResponse(BaseModel):
    id:        int
    name:      str
    email:     EmailStr
    role:      RoleEnum
    is_active: bool

    model_config = {"from_attributes": True}


# ── Modelo de respuesta envuelto (estandarizado) ──────────────────────────────
class UserListResponse(BaseModel):
    total:   int
    users:   list[UserResponse]
    