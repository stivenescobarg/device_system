from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.services.user_service import UserService
from app.dependencies.database_dependency import get_db

router = APIRouter()
user_service = UserService()


@router.get(
    "/users",
    response_model=list[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar todos los usuarios",
    description="Obtiene la lista de usuarios. Filtra por rol, estado activo y ordena por nombre o fecha.",
    tags=["Users"]
)
def get_users(
    response: Response,
    role:      Optional[str]  = None,
    is_active: Optional[bool] = None,
    order_by:  Optional[str]  = None,
    db: Session = Depends(get_db)
):
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "3.0"
    return user_service.get_all_users(db, role, is_active, order_by)


@router.get(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener usuario por ID",
    description="Retorna los datos de un usuario específico según su ID.",
    tags=["Users"]
)
def get_user(
    user_id: int,
    response: Response,
    db: Session = Depends(get_db)
):
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "3.0"
    user = user_service.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=f"Usuario con ID {user_id} no encontrado")
    return user


@router.post(
    "/users",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo usuario",
    description="Registra un nuevo usuario en la base de datos.",
    tags=["Users"]
)
def create_user(
    user: UserCreate,
    response: Response,
    db: Session = Depends(get_db)
):
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "3.0"
    return user_service.create_user(db, user)


@router.put(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario COMPLETAMENTE",
    description="Reemplaza TODOS los datos de un usuario existente.",
    tags=["Users"]
)
def update_user_complete(
    user_id: int,
    user: UserUpdate,
    response: Response,
    db: Session = Depends(get_db)
):
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "3.0"
    return user_service.update_user_complete(db, user_id, user)


@router.patch(
    "/users/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar usuario PARCIALMENTE",
    description="Modifica SOLO los campos enviados de un usuario existente.",
    tags=["Users"]
)
def update_user_partial(
    user_id: int,
    user: UserPatch,
    response: Response,
    db: Session = Depends(get_db)
):
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "3.0"
    return user_service.update_user_partial(db, user_id, user)


@router.delete(
    "/users/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar usuario",
    description="Elimina un usuario de la base de datos permanentemente.",
    tags=["Users"]
)
def delete_user(
    user_id: int,
    response: Response,
    db: Session = Depends(get_db)
):
    response.headers["X-App-Name"]    = "device_systems"
    response.headers["X-API-Version"] = "3.0"
    return user_service.delete_user(db, user_id)