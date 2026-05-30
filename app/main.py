from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.user_routes import router as user_router

# ── Instancia de la aplicación ────────────────────────────────────────────────
app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios del sistema **device_systems**.\n\n"
        "Permite crear, listar, filtrar y consultar usuarios con validaciones Pydantic v2."
    ),
    version="1.0.0",
    contact={"name": "device_systems Team"},
    license_info={"name": "MIT"},
)

# ── CORS (útil si conectas un frontend) ──────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Incluir rutas ─────────────────────────────────────────────────────────────
app.include_router(user_router)


# ── Ruta raíz ─────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "app":     "device_systems",
        "version": "1.0.0",
        "docs":    "/docs",
        "redoc":   "/redoc",
    }
