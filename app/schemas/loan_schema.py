from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum


class LoanStatus(str, Enum):
    active   = "active"
    returned = "returned"
    overdue  = "overdue"


class LoanCreate(BaseModel):
    user_id:   int = Field(..., description="ID del usuario que solicita el préstamo")
    device_id: int = Field(..., description="ID del dispositivo a prestar")

    model_config = {
        "json_schema_extra": {
            "examples": [{"user_id": 1, "device_id": 1}]
        }
    }


class LoanUpdate(BaseModel):
    status:      LoanStatus
    return_date: Optional[datetime] = None


class LoanResponse(BaseModel):
    id:          int
    user_id:     int
    device_id:   int
    loan_date:   Optional[datetime] = None
    return_date: Optional[datetime] = None
    status:      str

    model_config = {"from_attributes": True}


# ── Datos básicos del usuario, para anidar dentro del préstamo ───────────────
class UserBasic(BaseModel):
    id:    int
    name:  str
    email: str

    model_config = {"from_attributes": True}


# ── Datos básicos del dispositivo, para anidar dentro del préstamo ───────────
class DeviceBasic(BaseModel):
    id:            int
    name:          str
    serial_number: str
    device_type:   str

    model_config = {"from_attributes": True}


# ── Respuesta enriquecida con datos de usuario y dispositivo (para joins) ────
class LoanDetailResponse(BaseModel):
    loan_id:     int = Field(validation_alias="id")
    status:      str
    loan_date:   Optional[datetime] = None
    return_date: Optional[datetime] = None
    user:        UserBasic
    device:      DeviceBasic

    model_config = {"from_attributes": True, "populate_by_name": True}
