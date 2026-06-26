from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime


class DeviceCreate(BaseModel):
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
