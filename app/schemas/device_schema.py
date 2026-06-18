from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Schema para crear dispositivo
class DeviceCreate(BaseModel):
    name:          str            = Field(min_length=3, description="Nombre del dispositivo")
    serial_number: str             = Field(min_length=3, description="Número de serie único")
    device_type:   str             = Field(description="Tipo de dispositivo: laptop, tablet, proyector, cámara, router, monitor")
    brand:         Optional[str]   = Field(None, description="Marca del dispositivo")
    is_available:  bool            = Field(default=True, description="Disponibilidad del dispositivo")


# Schema para actualización COMPLETA (PUT)
class DeviceUpdate(BaseModel):
    name:          str            = Field(min_length=3)
    serial_number: str             = Field(min_length=3)
    device_type:   str
    brand:         Optional[str]   = None
    is_available:  bool


# Schema para actualización PARCIAL (PATCH)
class DevicePatch(BaseModel):
    name:          Optional[str]  = Field(None, min_length=3)
    serial_number: Optional[str]  = Field(None, min_length=3)
    device_type:   Optional[str]  = None
    brand:         Optional[str]  = None
    is_available:  Optional[bool] = None


# Schema de respuesta
class DeviceResponse(BaseModel):
    id:            int
    name:          str
    serial_number: str
    device_type:   str
    brand:         Optional[str]
    is_available:  bool
    created_at:    datetime

    model_config = {"from_attributes": True}