import re
from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional


class UserRegister(BaseModel):
    name:             str      = Field(..., min_length=3, description="Nombre completo, mínimo 3 caracteres")
    email:            EmailStr = Field(..., description="Correo electrónico válido y único")
    password:         str      = Field(..., description="Contraseña segura")
    role:             str      = Field(default="user", description="admin | support | user")

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

    @field_validator("password")
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("La contraseña debe tener al menos 8 caracteres")
        if not re.search(r"[A-Z]", v):
            raise ValueError("La contraseña debe contener al menos una mayúscula")
        if not re.search(r"[a-z]", v):
            raise ValueError("La contraseña debe contener al menos una minúscula")
        if not re.search(r"\d", v):
            raise ValueError("La contraseña debe contener al menos un número")
        if re.search(r"\s", v):
            raise ValueError("La contraseña no puede contener espacios en blanco")
        return v

    @field_validator("role")
    @classmethod
    def role_valid(cls, v: str) -> str:
        allowed = {"admin", "support", "user"}
        if v not in allowed:
            raise ValueError(f"Rol inválido. Permitidos: {allowed}")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "name": "Kelin Montoya",
                "email": "kelin@mail.com",
                "password": "Segura123",
                "role": "admin"
            }]
        }
    )


class UserLogin(BaseModel):
    email:    EmailStr = Field(..., description="Correo electrónico registrado")
    password: str      = Field(..., description="Contraseña")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{
                "email": "kelin@mail.com",
                "password": "Segura123"
            }]
        }
    )


class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"


class TokenData(BaseModel):
    email: Optional[str] = None
    role:  Optional[str] = None
