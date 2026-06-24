import time
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):
        # Generar o propagar X-Request-ID
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])

        # Medir tiempo de inicio
        start_time = time.time()

        # Procesar la petición
        response = await call_next(request)

        # Calcular tiempo de respuesta
        process_time = round(time.time() - start_time, 4)

        # Agregar cabeceras personalizadas
        response.headers["X-App-Name"]     = "device_systems"
        response.headers["X-Process-Time"] = str(process_time)
        response.headers["X-Request-ID"]   = request_id

        # Registrar en consola
        print(f"[{request_id}] {request.method} {request.url.path} → {response.status_code} ({process_time}s)")

        return response