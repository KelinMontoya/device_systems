from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine, Base
from app.models import User, Device, Loan  # noqa: F401 - registra los modelos en Base.metadata

from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

# Nota: en este proyecto las tablas se crean/actualizan mediante Alembic
# (alembic upgrade head). Se deja create_all como respaldo en desarrollo.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description=(
        "## API REST para gestión de usuarios, dispositivos y préstamos\n\n"
        "Sistema backend con **FastAPI + SQLAlchemy + Alembic** que permite "
        "gestionar usuarios, un inventario de dispositivos tecnológicos y el "
        "préstamo de dichos dispositivos a los usuarios.\n\n"
        "### Novedades v4.0\n"
        "- Migraciones de base de datos con **Alembic**\n"
        "- Nuevos recursos `Device` y `Loan` relacionados con `User`\n"
        "- Relaciones One-to-Many (`User` ⇄ `Loan`, `Device` ⇄ `Loan`)\n"
        "- Consultas con **joins** y filtros avanzados\n"
        "- Reglas de negocio: disponibilidad de dispositivos, devoluciones"
    ),
    version="4.0.0",
    contact={"name": "SENA - device_systems"},
    license_info={"name": "MIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "app":      "device_systems",
        "version":  "4.0.0",
        "database": "SQLite con SQLAlchemy + Alembic",
        "resources": ["/users", "/devices", "/loans"],
        "docs":     "/docs",
        "redoc":    "/redoc",
    }
