from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import engine, Base
from app.routes.user_routes import router as user_router

# Crear las tablas en la base de datos al iniciar la aplicación
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description=(
        "## API REST para gestión de usuarios\n\n"
        "Permite crear, listar, actualizar y eliminar usuarios "
        "del sistema **device_systems** con persistencia en base de datos SQLite.\n\n"
        "### Cambios v3.0\n"
        "- Persistencia real con **SQLAlchemy + SQLite**\n"
        "- Modelo `User` con constraints en base de datos\n"
        "- Schemas Pydantic separados del modelo ORM\n"
        "- CRUD completo sobre base de datos relacional"
    ),
    version="3.0.0",
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


@app.get("/", tags=["Root"])
def root():
    return {
        "app":      "device_systems",
        "version":  "3.0.0",
        "database": "SQLite con SQLAlchemy",
        "docs":     "/docs",
        "redoc":    "/redoc",
    }
