# Simulación de base de datos en memoria

users_db: list[dict] = [
    {"id": 1, "name": "Ana Torres",  "email": "ana@mail.com",   "role": "admin",   "is_active": True},
    {"id": 2, "name": "Luis Gomez",  "email": "luis@mail.com",  "role": "support", "is_active": True},
    {"id": 3, "name": "Maria Ruiz",  "email": "maria@mail.com", "role": "user",    "is_active": False},
    {"id": 4, "name": "Pedro Silva", "email": "pedro@mail.com", "role": "user",    "is_active": True},
]

id_counter: dict = {"value": 5}