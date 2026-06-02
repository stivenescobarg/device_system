from pydantic import BaseModel, EmailStr, Field
from enum import Enum
from typing import Optional

# Valores permitidos para el rol
class RoleEnum(str, Enum):
    admin = "admin"
    support = "support"
    user = "user"

# Modelo de entrada (para crear usuario)
class UserCreate(BaseModel):
    name: str = Field(min_length=3, description="Nombre del usuario, mínimo 3 caracteres")
    email: EmailStr = Field(description="Email válido del usuario")
    role: RoleEnum = Field(description="Rol del usuario: admin, support o user")
    is_active: bool = Field(description="Estado del usuario")

# Modelo para actualización COMPLETA (PUT)
class UserUpdate(BaseModel):
    name: str = Field(min_length=3, description="Nombre del usuario, mínimo 3 caracteres")
    email: EmailStr = Field(description="Email válido del usuario")
    role: RoleEnum = Field(description="Rol del usuario: admin, support o user")
    is_active: bool = Field(description="Estado del usuario")

# Modelo para actualización PARCIAL (PATCH)
class UserPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3, description="Nombre del usuario, mínimo 3 caracteres")
    email: Optional[EmailStr] = Field(None, description="Email válido del usuario")
    role: Optional[RoleEnum] = Field(None, description="Rol del usuario: admin, support o user")
    is_active: Optional[bool] = Field(None, description="Estado del usuario")

# Modelo de respuesta (lo que devuelve la API)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: RoleEnum
    is_active: bool