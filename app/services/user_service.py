from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch
from app.auth.security import get_password_hash


def get_all_users(db, role=None, is_active=None, order_by="id"):
    query = db.query(User)
    if role:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)
    order_map = {"name": User.name, "created_at": User.created_at}
    query = query.order_by(order_map.get(order_by, User.id))
    return query.all()


def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con id={user_id} no encontrado")
    return user


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, data: UserCreate) -> User:
    if get_user_by_email(db, str(data.email)):
        raise HTTPException(status_code=400, detail=f"El correo '{data.email}' ya está registrado")
    new_user = User(
        name=data.name,
        email=str(data.email),
        hashed_password=get_password_hash(data.password),
        role=data.role.value,
        is_active=data.is_active,
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Email duplicado")
    return new_user


def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
    user = get_user_by_id(db, user_id)
    existing = get_user_by_email(db, str(data.email))
    if existing and existing.id != user_id:
        raise HTTPException(status_code=400, detail="Email en uso por otro usuario")
    user.name = data.name
    user.email = str(data.email)
    user.role = data.role.value
    user.is_active = data.is_active
    db.commit()
    db.refresh(user)
    return user


def patch_user(db: Session, user_id: int, data: UserPatch) -> User:
    user = get_user_by_id(db, user_id)
    changes = data.model_dump(exclude_none=True)
    if not changes:
        raise HTTPException(status_code=400, detail="Debes enviar al menos un campo")
    if "email" in changes:
        existing = get_user_by_email(db, str(changes["email"]))
        if existing and existing.id != user_id:
            raise HTTPException(status_code=400, detail="Email ya en uso")
    for field, value in changes.items():
        setattr(user, field, value.value if hasattr(value, "value") else value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int) -> None:
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
