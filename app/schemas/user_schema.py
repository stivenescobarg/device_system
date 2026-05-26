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
    email: EmailStr = Field(description="Email válido del usuario") # email-validator Dependencia
    role: RoleEnum = Field(description="Rol del usuario: admin, support o user")
    is_active: bool = Field(description="Estado del usuario")

# Modelo de respuesta (lo que devuelve la API)
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: RoleEnum
    is_active: bool