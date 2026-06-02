from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.services.user_service import UserService
from app.dependencies.user_dependencies import (
    get_user_or_404,
    validate_unique_email,
    validate_unique_email_for_update,
    validate_role,
    get_api_config,
    get_current_user
)

router = APIRouter()

# Instancia del servicio
user_service = UserService()

# GET /users - Listar todos los usuarios
@router.get(
    "/users", 
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los usuarios",
    description="Obtiene la lista de usuarios con opción de filtrar por rol y estado activo",
    tags=["Users"]
)
def get_users(
    response: Response,
    role: Optional[str] = None, 
    is_active: Optional[bool] = None,
    config: dict = Depends(get_api_config)
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    
    # Validar rol si viene
    if role:
        validate_role(role)
    
    return user_service.get_all_users(role, is_active)


# GET /users/{user_id} - Obtener usuario por ID
@router.get(
    "/users/{user_id}", 
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="Retorna los datos de un usuario específico según su ID",
    tags=["Users"]
)
def get_user(
    user_id: int, 
    response: Response,
    user = Depends(get_user_or_404)
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    
    return user


# POST /users - Crear usuario
@router.post(
    "/users", 
    response_model=UserResponse, 
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo usuario",
    description="Registra un nuevo usuario en el sistema",
    tags=["Users"]
)
def create_user(
    user: UserCreate, 
    response: Response
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    
    # Validar email único
    validate_unique_email(user.email)
    
    # Validar rol
    validate_role(user.role.value)
    
    return user_service.create_user(user)


# PUT /users/{user_id} - Actualización COMPLETA
@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario COMPLETAMENTE",
    description="Reemplaza TODOS los datos de un usuario existente. Debe enviar todos los campos obligatorios.",
    tags=["Users"]
)
def update_user_complete(
    user_id: int, 
    user: UserUpdate, 
    response: Response,
    existing_user = Depends(get_user_or_404)
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    
    # Validar email único (excluyendo el propio usuario)
    validate_unique_email_for_update(user.email, user_id)
    
    # Validar rol
    validate_role(user.role.value)
    
    return user_service.update_user_complete(user_id, user)


# PATCH /users/{user_id} - Actualización PARCIAL
@router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario PARCIALMENTE",
    description="Modifica SOLO los campos enviados de un usuario existente. No es necesario enviar todos los campos.",
    tags=["Users"]
)
def update_user_partial(
    user_id: int, 
    user: UserPatch, 
    response: Response,
    existing_user = Depends(get_user_or_404)
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    
    # Validar email solo si viene en el PATCH
    if user.email:
        validate_unique_email_for_update(user.email, user_id)
    
    # Validar rol solo si viene en el PATCH
    if user.role:
        validate_role(user.role.value)
    
    return user_service.update_user_partial(user_id, user)


# DELETE /users/{user_id} - Eliminar usuario
@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar usuario",
    description="Elimina un usuario del sistema permanentemente",
    tags=["Users"]
)
def delete_user(
    user_id: int, 
    response: Response,
    existing_user = Depends(get_user_or_404)
):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"
    
    result = user_service.delete_user(user_id)
    return result