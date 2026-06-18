from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Schema para crear préstamo
class LoanCreate(BaseModel):
    user_id:   int = Field(description="ID del usuario que solicita el préstamo")
    device_id: int = Field(description="ID del dispositivo a prestar")


# Schema para actualizar préstamo (uso interno, ej. cambiar estado)
class LoanUpdate(BaseModel):
    status:      Optional[str]      = Field(None, description="Estado del préstamo: active, returned, overdue")
    return_date: Optional[datetime] = Field(None, description="Fecha de devolución")


# Schema de respuesta simple
class LoanResponse(BaseModel):
    id:          int
    user_id:     int
    device_id:   int
    loan_date:   datetime
    return_date: Optional[datetime]
    status:      str

    model_config = {"from_attributes": True}


class UserBasicInfo(BaseModel):
    id:    int
    name:  str
    email: str

    model_config = {"from_attributes": True}


class DeviceBasicInfo(BaseModel):
    id:            int
    name:          str
    serial_number: str
    device_type:   str

    model_config = {"from_attributes": True}


# Schema de respuesta con información relacionada (para joins)
class LoanDetailResponse(BaseModel):
    id:          int
    status:      str
    loan_date:   datetime
    return_date: Optional[datetime]
    user:        UserBasicInfo
    device:      DeviceBasicInfo

    model_config = {"from_attributes": True}