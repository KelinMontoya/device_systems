<<<<<<< HEAD
from pydantic import BaseModel, Field, ConfigDict
=======
from pydantic import BaseModel, Field
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
from typing import Optional
from datetime import datetime


class DeviceCreate(BaseModel):
<<<<<<< HEAD
    name:        str = Field(..., min_length=2, description="Nombre del dispositivo")
    serial:      str = Field(..., min_length=3, description="Número de serie único")
    brand:       str = Field(..., min_length=2, description="Marca del dispositivo")
    device_type: str = Field(..., description="laptop | desktop | tablet | phone | other")
    is_available: bool = Field(default=True)

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [{"name": "ThinkPad X1", "serial": "SN123ABC", "brand": "Lenovo", "device_type": "laptop"}]
        }
    )


class DeviceUpdate(BaseModel):
    name:        str
    serial:      str
    brand:       str
    device_type: str
    is_available: bool


class DevicePatch(BaseModel):
    name:        Optional[str]  = None
    serial:      Optional[str]  = None
    brand:       Optional[str]  = None
    device_type: Optional[str]  = None
    is_available: Optional[bool] = None


class DeviceResponse(BaseModel):
    id:          int
    name:        str
    serial:      str
    brand:       str
    device_type: str
    is_available: bool
    created_at:  Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
=======
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
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
