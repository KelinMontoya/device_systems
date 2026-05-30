from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import router as user_router

app = FastAPI(
    title="device_systems API",
    description=(
        "## API REST para gestión de usuarios\n\n"
        "Permite crear, listar, actualizar y eliminar usuarios "
        "del sistema **device_systems** con validaciones y manejo de errores."
    ),
    version="2.0.0",
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
        "app":     "device_systems",
        "version": "2.0.0",
        "docs":    "/docs",
        "redoc":   "/redoc",
    }