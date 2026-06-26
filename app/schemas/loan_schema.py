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


class LoanResponse(BaseModel):
    id:          int
    user_id:     int
    device_id:   int
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
