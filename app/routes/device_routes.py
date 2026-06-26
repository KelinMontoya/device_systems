from fastapi import APIRouter, Query, Path, Depends
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch, DeviceResponse
from app.services import device_service
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import require_admin, require_admin_or_support
from app.models.user_model import User

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get("/", response_model=list[DeviceResponse], summary="Listar dispositivos")
def get_devices(
    db: Session = Depends(get_db),
    device_type: Optional[str] = Query(None),
    is_available: Optional[bool] = Query(None),
    _: User = Depends(require_admin_or_support),
):
    return device_service.get_all_devices(db, device_type=device_type, is_available=is_available)


@router.get("/{device_id}", response_model=DeviceResponse, summary="Obtener dispositivo por ID")
def get_device(
    device_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_or_support),
):
    return device_service.get_device_by_id(db, device_id)


@router.post("/", response_model=DeviceResponse, status_code=201, summary="Crear dispositivo")
def create_device(
    data: DeviceCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_or_support),
):
    return device_service.create_device(db, data)


@router.put("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo")
def update_device(
    data: DeviceUpdate,
    device_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_or_support),
):
    return device_service.update_device(db, device_id, data)


@router.patch("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo parcial")
def patch_device(
    data: DevicePatch,
    device_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_or_support),
):
    return device_service.patch_device(db, device_id, data)


@router.delete("/{device_id}", status_code=204, summary="Eliminar dispositivo")
def delete_device(
    device_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    device_service.delete_device(db, device_id)
