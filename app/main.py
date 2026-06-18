from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.database.connection import create_tables

app = FastAPI(
    title="device_systems",
    description="API REST para gestión de usuarios, dispositivos y préstamos del sistema device_systems",
    version="4.0",
    contact={
        "name": "Stiven Escobar",
        "email": "stivenescobar240208@gmail.com"
    }
)

create_tables()

app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bienvenido a device_systems API",
        "version": "4.0",
        "endpoints": {
            "users":   "/users",
            "devices": "/devices",
            "loans":   "/loans",
            "docs":    "/docs",
            "redoc":   "/redoc"
        }
    }