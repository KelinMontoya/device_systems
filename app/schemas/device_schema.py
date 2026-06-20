from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class DeviceCreate(BaseModel):
    name:          str  = Field(..., min_length=2, description="Nombre del dispositivo")
    serial_number: str  = Field(..., min_length=3, description="Número de serie único")
    device_type:   str  = Field(..., description="laptop | tablet | proyector | camara | router | monitor")
    brand:         Optional[str] = Field(default=None, description="Marca del dispositivo")
    is_available:  bool = Field(default=True)

    model_config = {
        "json_schema_extra": {
            "examples": [{
                "name": "Laptop Lenovo ThinkPad",
                "serial_number": "LEN-2024-001",
                "device_type": "laptop",
                "brand": "Lenovo",
                "is_available": True
            }]
        }
    }


class DeviceUpdate(BaseModel):
    name:          str  = Field(..., min_length=2)
    serial_number: str  = Field(..., min_length=3)
    device_type:   str
    brand:         Optional[str] = None
    is_available:  bool


class DevicePatch(BaseModel):
    name:          Optional[str]  = Field(default=None, min_length=2)
    serial_number: Optional[str]  = Field(default=None, min_length=3)
    device_type:   Optional[str]  = None
    brand:         Optional[str]  = None
    is_available:  Optional[bool] = None


class DeviceResponse(BaseModel):
    id:            int
    name:          str
    serial_number: str
    device_type:   str
    brand:         Optional[str] = None
    is_available:  bool
    created_at:    Optional[datetime] = None

    model_config = {"from_attributes": True}


# ── Versión resumida para anidar en LoanDetailResponse ────────────────────────
class DeviceBasic(BaseModel):
    id:            int
    name:          str
    serial_number: str
    device_type:   str

    model_config = {"from_attributes": True}
