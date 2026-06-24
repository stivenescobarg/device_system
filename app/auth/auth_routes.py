from fastapi import APIRouter, Depends, status, Request
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.schemas.auth_schema import UserRegister, UserLogin, Token, UserAuthResponse
from app.auth.auth_service import AuthService
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import get_current_active_user

router = APIRouter(prefix="/auth", tags=["Auth"])
auth_service = AuthService()
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/register",
    response_model=UserAuthResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar nuevo usuario",
    description="Crea un nuevo usuario con contraseña segura. La contraseña se almacena como hash, nunca en texto plano.",
    response_description="Usuario registrado exitosamente"
)
@limiter.limit("3/minute")
def register(request: Request, user_data: UserRegister, db: Session = Depends(get_db)):
    return auth_service.register_user(db, user_data)


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión",
    description="Autentica al usuario y retorna un token JWT para acceder a rutas protegidas.",
    response_description="Token de acceso generado"
)
@limiter.limit("5/minute")
def login(request: Request, user_data: UserLogin, db: Session = Depends(get_db)):
    return auth_service.login_user(db, user_data.email, user_data.password)


@router.get(
    "/me",
    response_model=UserAuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario autenticado",
    description="Retorna los datos del usuario autenticado usando el token JWT. No expone la contraseña.",
    response_description="Datos del usuario autenticado"
)
def get_me(current_user=Depends(get_current_active_user)):
    return current_user