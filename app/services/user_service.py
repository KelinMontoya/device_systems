from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch


# ── Listar usuarios (con filtros opcionales) ──────────────────────────────────
def get_all_users(
    db: Session,
    role: str = None,
    is_active: bool = None,
    order_by: str = "id"
) -> list[User]:
    query = db.query(User)

    if role is not None:
        query = query.filter(User.role == role)
    if is_active is not None:
        query = query.filter(User.is_active == is_active)

    # Ordenar por nombre o fecha de creación
    if order_by == "name":
        query = query.order_by(User.name)
    elif order_by == "created_at":
        query = query.order_by(User.created_at)
    else:
        query = query.order_by(User.id)

    return query.all()


# ── Buscar por ID ─────────────────────────────────────────────────────────────
def get_user_by_id(db: Session, user_id: int) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con id={user_id} no encontrado"
        )
    return user


# ── Buscar por email ──────────────────────────────────────────────────────────
def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


# ── Crear usuario ─────────────────────────────────────────────────────────────
def create_user(db: Session, data: UserCreate) -> User:
    # Verificar email duplicado antes de insertar
    if get_user_by_email(db, str(data.email)):
        raise HTTPException(
            status_code=400,
            detail=f"El correo '{data.email}' ya está registrado"
        )

    new_user = User(
        name=data.name,
        email=str(data.email),
        role=data.role.value,
        is_active=data.is_active,
    )
    db.add(new_user)
    try:
        db.commit()
        db.refresh(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"El correo '{data.email}' ya está registrado (constraint)"
        )
    return new_user


# ── Actualizar completo (PUT) ─────────────────────────────────────────────────
def update_user(db: Session, user_id: int, data: UserUpdate) -> User:
    user = get_user_by_id(db, user_id)

    # Verificar email duplicado ignorando el propio usuario
    existing = get_user_by_email(db, str(data.email))
    if existing and existing.id != user_id:
        raise HTTPException(
            status_code=400,
            detail=f"El correo '{data.email}' ya está en uso por otro usuario"
        )

    user.name      = data.name
    user.email     = str(data.email)
    user.role      = data.role.value
    user.is_active = data.is_active

    db.commit()
    db.refresh(user)
    return user


# ── Actualizar parcial (PATCH) ────────────────────────────────────────────────
def patch_user(db: Session, user_id: int, data: UserPatch) -> User:
    user    = get_user_by_id(db, user_id)
    changes = data.model_dump(exclude_none=True)

    if not changes:
        raise HTTPException(
            status_code=400,
            detail="Debes enviar al menos un campo para actualizar"
        )

    if "email" in changes:
        existing = get_user_by_email(db, str(changes["email"]))
        if existing and existing.id != user_id:
            raise HTTPException(
                status_code=400,
                detail=f"El correo '{changes['email']}' ya está en uso"
            )

    for field, value in changes.items():
        # Convertir RoleEnum a string si es necesario
        if hasattr(value, "value"):
            value = value.value
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user


# ── Eliminar usuario ──────────────────────────────────────────────────────────
def delete_user(db: Session, user_id: int) -> None:
    user = get_user_by_id(db, user_id)
    db.delete(user)
    db.commit()
