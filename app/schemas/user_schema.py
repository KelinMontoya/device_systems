from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from enum import Enum
from datetime import datetime


class RoleEnum(str, Enum):
    admin   = "admin"
    support = "support"
    user    = "user"


# ── Entrada para CREATE (POST) ────────────────────────────────────────────────
class UserCreate(BaseModel):
    name:      str      = Field(..., min_length=3, description="Mínimo 3 caracteres")
    email:     EmailStr = Field(..., description="Correo electrónico válido")
    role:      RoleEnum = Field(..., description="admin | support | user")
    is_active: bool     = Field(default=True)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "Sofia Leon",
                "email": "sofia@mail.com",
                "role": "support",
                "is_active": True
            }]
        }
    }


# ── Entrada para UPDATE completo (PUT) ───────────────────────────────────────
class UserUpdate(BaseModel):
    name:      str      = Field(..., min_length=3)
    email:     EmailStr
    role:      RoleEnum
    is_active: bool


# ── Entrada para UPDATE parcial (PATCH) ──────────────────────────────────────
class UserPatch(BaseModel):
    name:      Optional[str]      = Field(default=None, min_length=3)
    email:     Optional[EmailStr] = None
    role:      Optional[RoleEnum] = None
    is_active: Optional[bool]     = None


# ── Salida (RESPONSE) ─────────────────────────────────────────────────────────
class UserResponse(BaseModel):
    id:         int
    name:       str
    email:      EmailStr
    role:       RoleEnum
    is_active:  bool
    created_at: Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Respuesta de error estructurada ──────────────────────────────────────────
class ErrorResponse(BaseModel):
    error:       bool = True
    message:     str
    status_code: int
