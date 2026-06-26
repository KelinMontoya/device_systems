import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware personalizado que:
    - Mide el tiempo de respuesta
    - Agrega cabeceras X-Process-Time, X-App-Name y X-Request-ID
    - Registra método, ruta y código de estado de cada petición
    """

    async def dispatch(self, request: Request, call_next):
        start_time    = time.time()
        request_id    = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])

        response      = await call_next(request)

        process_time  = round(time.time() - start_time, 6)

        response.headers["X-App-Name"]     = "device_systems"
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"]   = request_id

        print(
            f"[{request_id}] {request.method} {request.url.path} "
            f"→ {response.status_code} ({process_time}s)"
        )

        return response
