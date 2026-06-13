from app.database.connection import SessionLocal


def get_db():
    """
    Dependencia que entrega una sesión de base de datos.
    Se usa con Depends() en los endpoints.
    Garantiza que la sesión se cierre al terminar cada request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
