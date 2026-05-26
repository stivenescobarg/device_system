from fastapi import FastAPI
from app.routes.user_routes import router

# Crear la instancia de la aplicación
app = FastAPI(
    title="device_systems",
    description="API REST para gestión de usuarios del sistema device_systems",
    version="1.0"
)

# Registrar las rutas
app.include_router(router)