<<<<<<< HEAD
from fastapi import APIRouter, Query, Path, Depends
=======
from fastapi import APIRouter, Query, Response, Path, Depends
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch, DeviceResponse
<<<<<<< HEAD
from app.services import device_service
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import require_admin, require_admin_or_support
from app.models.user_model import User
=======
from app.schemas.loan_schema import LoanDetailResponse
from app.services import device_service, loan_service
from app.dependencies.database_dependency import get_db
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf

router = APIRouter(prefix="/devices", tags=["Devices"])


<<<<<<< HEAD
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
=======
@router.get(
    "/",
    response_model=list[DeviceResponse],
    summary="Listar dispositivos",
    description="Retorna todos los dispositivos. Permite filtrar por tipo, disponibilidad, marca o búsqueda libre.",
)
def get_devices(
    db:           Session         = Depends(get_db),
    device_type:  Optional[str]   = Query(None, description="laptop | tablet | proyector | camara | router | monitor"),
    is_available: Optional[bool]  = Query(None),
    brand:        Optional[str]   = Query(None),
    search:       Optional[str]   = Query(None, description="Busca en nombre o número de serie"),
):
    return device_service.get_all_devices(
        db, device_type=device_type, is_available=is_available, brand=brand, search=search
    )


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Obtener dispositivo por ID",
    responses={404: {"description": "Dispositivo no encontrado"}},
)
def get_device(
    device_id: int     = Path(..., ge=1),
    db:        Session = Depends(get_db),
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
):
    return device_service.get_device_by_id(db, device_id)


<<<<<<< HEAD
@router.post("/", response_model=DeviceResponse, status_code=201, summary="Crear dispositivo")
def create_device(
    data: DeviceCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_or_support),
=======
@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=201,
    summary="Crear dispositivo",
    description="Registra un nuevo dispositivo. El número de serie debe ser único.",
    responses={400: {"description": "Número de serie duplicado"}},
)
def create_device(
    data: DeviceCreate,
    db:   Session = Depends(get_db),
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
):
    return device_service.create_device(db, data)


<<<<<<< HEAD
@router.put("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo")
def update_device(
    data: DeviceUpdate,
    device_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_or_support),
=======
@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo completo",
    responses={404: {"description": "No encontrado"}, 400: {"description": "Serial duplicado"}},
)
def update_device(
    data:      DeviceUpdate,
    device_id: int     = Path(..., ge=1),
    db:        Session = Depends(get_db),
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
):
    return device_service.update_device(db, device_id, data)


<<<<<<< HEAD
@router.patch("/{device_id}", response_model=DeviceResponse, summary="Actualizar dispositivo parcial")
def patch_device(
    data: DevicePatch,
    device_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin_or_support),
=======
@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    summary="Actualizar dispositivo parcial",
    responses={404: {"description": "No encontrado"}},
)
def patch_device(
    data:      DevicePatch,
    device_id: int     = Path(..., ge=1),
    db:        Session = Depends(get_db),
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
):
    return device_service.patch_device(db, device_id, data)


<<<<<<< HEAD
@router.delete("/{device_id}", status_code=204, summary="Eliminar dispositivo")
def delete_device(
    device_id: int = Path(..., ge=1),
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
):
    device_service.delete_device(db, device_id)
=======
@router.delete(
    "/{device_id}",
    status_code=204,
    summary="Eliminar dispositivo",
    responses={404: {"description": "No encontrado"}},
)
def delete_device(
    device_id: int     = Path(..., ge=1),
    db:        Session = Depends(get_db),
):
    device_service.delete_device(db, device_id)


# ── GET /devices/{device_id}/loans ────────────────────────────────────────────
@router.get(
    "/{device_id}/loans",
    response_model=list[LoanDetailResponse],
    summary="Historial de préstamos de un dispositivo",
    description="Retorna el historial completo de préstamos de un dispositivo, incluyendo datos del usuario (JOIN).",
    responses={404: {"description": "Dispositivo no encontrado"}},
)
def get_device_loans(
    device_id: int     = Path(..., ge=1),
    db:        Session = Depends(get_db),
):
    return loan_service.get_loans_by_device(db, device_id)
>>>>>>> 5889c123adb2e89054014a752d482405d763f8cf
