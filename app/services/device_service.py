from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch


def get_all_devices(db: Session, device_type=None, is_available=None):
    query = db.query(Device)
    if device_type:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    return query.all()


def get_device_by_id(db: Session, device_id: int) -> Device:
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(status_code=404, detail=f"Dispositivo id={device_id} no encontrado")
    return device


def create_device(db: Session, data: DeviceCreate) -> Device:
    existing = db.query(Device).filter(Device.serial == data.serial).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"El serial '{data.serial}' ya existe")
    device = Device(**data.model_dump())
    db.add(device)
    try:
        db.commit()
        db.refresh(device)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Serial duplicado")
    return device


def update_device(db: Session, device_id: int, data: DeviceUpdate) -> Device:
    device = get_device_by_id(db, device_id)
    existing = db.query(Device).filter(Device.serial == data.serial).first()
    if existing and existing.id != device_id:
        raise HTTPException(status_code=400, detail="Serial en uso")
    for field, value in data.model_dump().items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def patch_device(db: Session, device_id: int, data: DevicePatch) -> Device:
    device  = get_device_by_id(db, device_id)
    changes = data.model_dump(exclude_none=True)
    if not changes:
        raise HTTPException(status_code=400, detail="Envía al menos un campo")
    for field, value in changes.items():
        setattr(device, field, value)
    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device_id: int) -> None:
    device = get_device_by_id(db, device_id)
    db.delete(device)
    db.commit()
