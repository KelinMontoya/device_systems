from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.database.connection import engine, Base
from app.middlewares.request_middleware import RequestLoggingMiddleware

# Importar todos los modelos para que SQLAlchemy los registre
from app.models import user_model, device_model, loan_model  # noqa: F401

from app.auth.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router

# ── Crear tablas ──────────────────────────────────────────────────────────────
Base.metadata.create_all(bind=engine)

# ── Rate Limiter global ───────────────────────────────────────────────────────
limiter = Limiter(key_func=get_remote_address)

# ── Aplicación FastAPI ────────────────────────────────────────────────────────
app = FastAPI(
    title="device_systems API",
    description=(
        "## API REST segura para gestión de usuarios, dispositivos y préstamos\n\n"
        "### Versión 4.0 — Seguridad y Autenticación\n"
        "- **OAuth2 + JWT** para autenticación\n"
        "- **Hash bcrypt** para contraseñas seguras\n"
        "- **Roles y autorización** (admin, support, user)\n"
        "- **Middleware** de trazabilidad con X-Process-Time y X-Request-ID\n"
        "- **CORS** configurado para clientes frontend autorizados\n"
        "- **Rate Limiting** para prevenir abuso de endpoints\n"
        "- **Pydantic v2** con validaciones avanzadas\n"
    ),
    version="4.0.0",
    contact={"name": "SENA ADSO - Kelin Montoya"},
    license_info={"name": "MIT"},
)

# ── Estado del rate limiter ───────────────────────────────────────────────────
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ── Middleware de trazabilidad (primero, envuelve todo) ───────────────────────
app.add_middleware(RequestLoggingMiddleware)

# ── CORS ──────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────────────────────────────────
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


# ── Root ──────────────────────────────────────────────────────────────────────
@app.get("/", tags=["Root"])
def root():
    return {
        "app":      "device_systems",
        "version":  "4.0.0",
        "database": "SQLite + SQLAlchemy",
        "security": "OAuth2 + JWT + bcrypt",
        "docs":     "/docs",
        "redoc":    "/redoc",
    }
