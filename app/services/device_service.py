from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import or_
from fastapi import HTTPException

from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch


def get_all_devices(
    db: Session,
    device_type: str = None,
    is_available: bool = None,
    brand: str = None,
    search: str = None,
) -> list[Device]:
    query = db.query(Device)

    if device_type is not None:
        query = query.filter(Device.device_type == device_type)
    if is_available is not None:
        query = query.filter(Device.is_available == is_available)
    if brand is not None:
        query = query.filter(Device.brand.ilike(f"%{brand}%"))
    if search is not None:
        query = query.filter(
            or_(
                Device.name.ilike(f"%{search}%"),
                Device.serial_number.ilike(f"%{search}%"),
            )
        )

    return query.order_by(Device.id).all()


def get_device_by_id(db: Session, device_id: int) -> Device:
    device = db.query(Device).filter(Device.id == device_id).first()
    if not device:
        raise HTTPException(
            status_code=404,
            detail=f"Dispositivo con id={device_id} no encontrado"
        )
    return device


def get_device_by_serial(db: Session, serial_number: str) -> Device | None:
    return db.query(Device).filter(Device.serial_number == serial_number).first()


def create_device(db: Session, data: DeviceCreate) -> Device:
    if get_device_by_serial(db, data.serial_number):
        raise HTTPException(
            status_code=400,
            detail=f"El número de serie '{data.serial_number}' ya está registrado"
        )

    new_device = Device(**data.model_dump())
    db.add(new_device)
    try:
        db.commit()
        db.refresh(new_device)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Número de serie duplicado")
    return new_device


def update_device(db: Session, device_id: int, data: DeviceUpdate) -> Device:
    device = get_device_by_id(db, device_id)

    existing = get_device_by_serial(db, data.serial_number)
    if existing and existing.id != device_id:
        raise HTTPException(
            status_code=400,
            detail=f"El número de serie '{data.serial_number}' ya está en uso"
        )

    for field, value in data.model_dump().items():
        setattr(device, field, value)

    db.commit()
    db.refresh(device)
    return device


def patch_device(db: Session, device_id: int, data: DevicePatch) -> Device:
    device  = get_device_by_id(db, device_id)
    changes = data.model_dump(exclude_none=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="Debes enviar al menos un campo para actualizar"
        )

    if "serial_number" in changes:
        existing = get_device_by_serial(db, changes["serial_number"])
        if existing and existing.id != device_id:
            raise HTTPException(status_code=400, detail="Número de serie ya en uso")

    for field, value in changes.items():
        setattr(device, field, value)

    db.commit()
    db.refresh(device)
    return device


def delete_device(db: Session, device_id: int) -> None:
    device = get_device_by_id(db, device_id)
    db.delete(device)
    db.commit()
