from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.routes.user_routes import router as user_router
from app.routes.device_routes import router as device_router
from app.routes.loan_routes import router as loan_router
from app.auth.auth_routes import router as auth_router
from app.database.connection import create_tables
from app.middlewares.request_middleware import RequestMiddleware

# Configurar limiter global
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="device_systems API",
    description="API REST segura para gestión de usuarios, dispositivos y préstamos",
    version="5.0",
    contact={
        "name": "Stiven Escobar",
        "email": "stivenescobar240208@gmail.com"
    }
)

# Rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Middlewares
app.add_middleware(RequestMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

create_tables()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(device_router)
app.include_router(loan_router)


@app.get("/", tags=["Root"])
def root():
    return {
        "message": "Bienvenido a device_systems API",
        "version": "5.0",
        "endpoints": {
            "auth":    "/auth",
            "users":   "/users",
            "devices": "/devices",
            "loans":   "/loans",
            "docs":    "/docs",
            "redoc":   "/redoc"
        }
    }