from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from typing import Optional
import re


class UserRegister(BaseModel):
    name:     str      = Field(min_length=3, description="Nombre del usuario")
    email:    EmailStr = Field(description="Email válido del usuario")
    password: str      = Field(min_length=8, description="Contraseña segura")
    role:     str      = Field(default="user", description="Rol: admin, support, user")

    @field_validator("password")
    @classmethod
    def validate_password(cls, value):
        if " " in value:
            raise ValueError("La contraseña no puede contener espacios")
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe tener al menos una mayúscula")
        if not re.search(r"[a-z]", value):
            raise ValueError("La contraseña debe tener al menos una minúscula")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe tener al menos un número")
        return value

    @field_validator("role")
    @classmethod
    def validate_role(cls, value):
        allowed = ["admin", "support", "user"]
        if value not in allowed:
            raise ValueError(f"Rol no permitido. Roles válidos: {', '.join(allowed)}")
        return value


class UserLogin(BaseModel):
    email:    EmailStr = Field(description="Email del usuario")
    password: str      = Field(description="Contraseña del usuario")


class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"


class TokenData(BaseModel):
    email:   Optional[str] = None
    role:    Optional[str] = None


class UserAuthResponse(BaseModel):
    id:        int
    name:      str
    email:     str
    role:      str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)