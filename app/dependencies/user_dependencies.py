from fastapi import HTTPException, status
from typing import Optional
from app.data.users_db import users_db
from app.services.user_service import UserService

# Instancia del servicio
user_service = UserService()


# Dependencia 1: Obtener usuario por ID o lanzar 404
def get_user_or_404(user_id: int):
    """
    Dependencia que busca un usuario por ID.
    Si no existe, lanza excepción 404.
    """
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con ID {user_id} no encontrado"
        )
    return user


# Dependencia 2: Validar que el email no exista (para crear)
def validate_unique_email(email: str):
    """
    Dependencia que valida que el email no esté registrado.
    Si existe, lanza excepción 400.
    """
    existing_user = user_service.get_user_by_email(email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El email {email} ya está registrado"
        )
    return email


# Dependencia 3: Validar email único al actualizar (excluyendo el propio ID)
def validate_unique_email_for_update(email: str, user_id: int):
    """
    Dependencia que valida que el email no esté registrado por OTRO usuario.
    """
    existing_user = user_service.get_user_by_email(email)
    if existing_user and existing_user["id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El email {email} ya está registrado por otro usuario"
        )
    return email


# Dependencia 4: Validar que el rol sea permitido
def validate_role(role: str):
    """
    Dependencia que valida que el rol sea admin, support o user.
    """
    allowed_roles = ["admin", "support", "user"]
    if role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Rol '{role}' no permitido. Roles válidos: {', '.join(allowed_roles)}"
        )
    return role


# Dependencia 5: Obtener configuración de la API
def get_api_config():
    """
    Dependencia que retorna configuración general de la API.
    """
    return {
        "app_name": "device_systems",
        "version": "2.0",
        "description": "API REST para gestión de usuarios"
    }


# Dependencia 6: Simular autenticación básica
def get_current_user(authorization: Optional[str] = None):
    """
    Dependencia que simula autenticación.
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Se requiere token de autenticación"
        )
    
    if authorization != "Bearer admin-token":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado"
        )
    
    return {"user_id": 1, "username": "admin", "role": "admin"}