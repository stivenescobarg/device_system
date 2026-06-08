from fastapi import FastAPI
from app.routes.user_routes import router
from app.database.connection import create_tables

app = FastAPI(
    title="device_systems",
    description="API REST para gestión de usuarios del sistema device_systems",
    version="3.0",
    contact={
        "name": "Stiven Escobar",
        "email": "stivenescobar240208@gmail.com"
    }
)

create_tables()

app.include_router(router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bienvenido a device_systems API",
        "version": "3.0",
        "endpoints": {
            "users": "/users",
            "docs":  "/docs",
            "redoc": "/redoc"
        }
    }