<<<<<<< HEAD
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class LoanCreate(BaseModel):
    user_id:   int = Field(..., ge=1, description="ID del usuario")
    device_id: int = Field(..., ge=1, description="ID del dispositivo")
    notes:     Optional[str] = Field(default=None, description="Observaciones del préstamo")

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"user_id": 1, "device_id": 1, "notes": "Préstamo para trabajo remoto"}]}
    )
=======
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
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf


class LoanResponse(BaseModel):
    id:          int
    user_id:     int
    device_id:   int
<<<<<<< HEAD
    loan_date:   datetime
    return_date: Optional[datetime] = None
    is_returned: bool
    notes:       Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class LoanDetail(BaseModel):
    id:           int
    loan_date:    datetime
    return_date:  Optional[datetime] = None
    is_returned:  bool
    notes:        Optional[str] = None
    user_name:    str
    user_email:   str
    device_name:  str
    device_serial: str
    device_brand: str

    model_config = ConfigDict(from_attributes=True)
=======
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
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
