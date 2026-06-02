from fastapi import FastAPI
from app.routes.user_routes import router

# Crear la instancia de la aplicación con metadatos mejorados
app = FastAPI(
    title="device_systems",
    description="API REST para gestión de usuarios del sistema device_systems",
    version="2.0",  # Actualizado a versión 2.0 por los nuevos endpoints
    contact={
        "name": "Stiven Escobar",
        "email": "stivenescobar240208@gmail.com"
    }
)

# Registrar las rutas
app.include_router(router)

# Ruta raíz
@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bienvenido a device_systems API",
        "version": "2.0",
        "endpoints": {
            "users": "/users",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }