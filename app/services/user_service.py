from fastapi import HTTPException
from app.data.users_db import users_db, id_counter
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch


def get_all_users(role: str = None, is_active: bool = None) -> list[dict]:
    result = list(users_db)
    if role is not None:
        result = [u for u in result if u["role"] == role]
    if is_active is not None:
        result = [u for u in result if u["is_active"] == is_active]
    return result


def get_user_by_id(user_id: int) -> dict:
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con id={user_id} no encontrado"
        )
    return user


def create_user(data: UserCreate) -> dict:
    if any(u["email"] == data.email for u in users_db):
        raise HTTPException(
            status_code=400,
            detail=f"El correo '{data.email}' ya está registrado"
        )
    new_user = {"id": id_counter["value"], **data.model_dump()}
    id_counter["value"] += 1
    users_db.append(new_user)
    return new_user


def update_user(user_id: int, data: UserUpdate) -> dict:
    user = get_user_by_id(user_id)

    # Verificar email duplicado (ignorar el propio usuario)
    if any(u["email"] == data.email and u["id"] != user_id for u in users_db):
        raise HTTPException(
            status_code=400,
            detail=f"El correo '{data.email}' ya está en uso por otro usuario"
        )

    user.update(data.model_dump())
    return user


def patch_user(user_id: int, data: UserPatch) -> dict:
    user = get_user_by_id(user_id)

    # Verificar que se envió al menos un campo
    changes = data.model_dump(exclude_none=True)
    if not changes:
        raise HTTPException(
            status_code=400,
            detail="Debes enviar al menos un campo para actualizar"
        )

    # Verificar email duplicado si se está cambiando
    if "email" in changes:
        if any(u["email"] == changes["email"] and u["id"] != user_id for u in users_db):
            raise HTTPException(
                status_code=400,
                detail=f"El correo '{changes['email']}' ya está en uso"
            )

    user.update(changes)
    return user


def delete_user(user_id: int) -> None:
    user = get_user_by_id(user_id)
    users_db.remove(user)