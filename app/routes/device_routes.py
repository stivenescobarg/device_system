from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch, DeviceResponse
from app.services.device_service import DeviceService
from app.dependencies.database_dependency import get_db
from app.dependencies.auth_dependency import (
    get_current_active_user,
    require_admin,
    require_admin_or_support
)

router = APIRouter()
device_service = DeviceService()


@router.get(
    "/devices",
    response_model=list[DeviceResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar dispositivos",
    description="Obtiene la lista de dispositivos. Requiere autenticación.",
    tags=["Devices"]
)
def get_devices(
    device_type:  Optional[str]  = None,
    is_available: Optional[bool] = None,
    brand:        Optional[str]  = None,
    search:       Optional[str]  = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    return device_service.get_all_devices(db, device_type, is_available, brand, search)


@router.get(
    "/devices/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener dispositivo por ID",
    description="Retorna los datos de un dispositivo. Requiere autenticación.",
    tags=["Devices"]
)
def get_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail=f"Dispositivo con ID {device_id} no encontrado")
    return device


@router.post(
    "/devices",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo dispositivo",
    description="Registra un nuevo dispositivo. Requiere rol admin o support.",
    tags=["Devices"]
)
def create_device(
    device: DeviceCreate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin_or_support)
):
    return device_service.create_device(db, device)


@router.put(
    "/devices/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar dispositivo COMPLETAMENTE",
    description="Requiere rol admin o support.",
    tags=["Devices"]
)
def update_device_complete(
    device_id: int,
    device: DeviceUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin_or_support)
):
    return device_service.update_device_complete(db, device_id, device)


@router.patch(
    "/devices/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar dispositivo PARCIALMENTE",
    description="Requiere rol admin o support.",
    tags=["Devices"]
)
def update_device_partial(
    device_id: int,
    device: DevicePatch,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin_or_support)
):
    return device_service.update_device_partial(db, device_id, device)


@router.delete(
    "/devices/{device_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo permanentemente. Requiere rol admin.",
    tags=["Devices"]
)
def delete_device(
    device_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(require_admin)
):
    return device_service.delete_device(db, device_id)