from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch, DeviceResponse
from app.services.device_service import DeviceService
from app.dependencies.database_dependency import get_db

router = APIRouter()
device_service = DeviceService()


@router.get(
    "/devices",
    response_model=list[DeviceResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar dispositivos",
    description="Obtiene la lista de dispositivos. Permite filtrar por tipo, disponibilidad, marca o búsqueda por nombre/serie.",
    response_description="Lista de dispositivos",
    tags=["Devices"]
)
def get_devices(
    device_type:  Optional[str]  = None,
    is_available: Optional[bool] = None,
    brand:        Optional[str]  = None,
    search:       Optional[str]  = None,
    db: Session = Depends(get_db)
):
    return device_service.get_all_devices(db, device_type, is_available, brand, search)


@router.get(
    "/devices/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener dispositivo por ID",
    description="Retorna los datos de un dispositivo específico según su ID.",
    response_description="Dispositivo encontrado",
    tags=["Devices"]
)
def get_device(device_id: int, db: Session = Depends(get_db)):
    device = device_service.get_device_by_id(db, device_id)
    if not device:
        raise HTTPException(status_code=404, detail=f"Dispositivo con ID {device_id} no encontrado")
    return device


@router.post(
    "/devices",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear nuevo dispositivo",
    description="Registra un nuevo dispositivo en el sistema.",
    response_description="Dispositivo creado",
    tags=["Devices"]
)
def create_device(device: DeviceCreate, db: Session = Depends(get_db)):
    return device_service.create_device(db, device)


@router.put(
    "/devices/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar dispositivo COMPLETAMENTE",
    description="Reemplaza todos los datos de un dispositivo existente.",
    response_description="Dispositivo actualizado",
    tags=["Devices"]
)
def update_device_complete(device_id: int, device: DeviceUpdate, db: Session = Depends(get_db)):
    return device_service.update_device_complete(db, device_id, device)


@router.patch(
    "/devices/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualizar dispositivo PARCIALMENTE",
    description="Modifica solo los campos enviados de un dispositivo existente.",
    response_description="Dispositivo actualizado parcialmente",
    tags=["Devices"]
)
def update_device_partial(device_id: int, device: DevicePatch, db: Session = Depends(get_db)):
    return device_service.update_device_partial(db, device_id, device)


@router.delete(
    "/devices/{device_id}",
    status_code=status.HTTP_200_OK,
    summary="Eliminar dispositivo",
    description="Elimina un dispositivo del sistema permanentemente.",
    response_description="Confirmación de eliminación",
    tags=["Devices"]
)
def delete_device(device_id: int, db: Session = Depends(get_db)):
    return device_service.delete_device(db, device_id)