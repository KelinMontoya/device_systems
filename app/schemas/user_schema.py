from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional
from enum import Enum
from datetime import datetime


class RoleEnum(str, Enum):
    admin   = "admin"
    support = "support"
    user    = "user"


class UserCreate(BaseModel):
    name:      str      = Field(..., min_length=3, description="Mínimo 3 caracteres")
    email:     EmailStr = Field(..., description="Correo electrónico válido")
    password:  str      = Field(..., description="Contraseña segura")
    role:      RoleEnum = Field(default=RoleEnum.user, description="admin | support | user")
    is_active: bool     = Field(default=True)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v: str) -> str:
        if v.strip() == "":
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"name": "Sofia Leon", "email": "sofia@mail.com", "password": "Segura123", "role": "support"}]
        }
    )


class UserUpdate(BaseModel):
    name:      str      = Field(..., min_length=3)
    email:     EmailStr
    role:      RoleEnum
    is_active: bool


class UserPatch(BaseModel):
    name:      Optional[str]      = Field(default=None, min_length=3)
    email:     Optional[EmailStr] = None
    role:      Optional[RoleEnum] = None
    is_active: Optional[bool]     = None


class UserResponse(BaseModel):
    id:         int
    name:       str
    email:      EmailStr
    role:       str
    is_active:  bool
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    error:       bool = True
    message:     str
    status_code: int
