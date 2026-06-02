from fastapi import HTTPException, status
from typing import List, Optional, Dict, Any
from app.data.users_db import users_db, get_next_id
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch

class UserService:
    """Servicio con toda la lógica de negocio para usuarios"""
    
    def __init__(self):
        self.db = users_db
    
    def get_all_users(self, role: Optional[str] = None, is_active: Optional[bool] = None) -> List[Dict[str, Any]]:
        """Obtiene todos los usuarios con filtros opcionales"""
        result = self.db
        
        if role:
            result = [u for u in result if u["role"] == role]
        
        if is_active is not None:
            result = [u for u in result if u["is_active"] == is_active]
        
        return result
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Busca usuario por ID (sin lanzar excepción, para que la dependencia la lance)"""
        return next((u for u in self.db if u["id"] == user_id), None)
    
    def get_user_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        """Busca usuario por email"""
        return next((u for u in self.db if u["email"] == email), None)
    
    def create_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """Crea un nuevo usuario (sin validaciones, las hace Depends)"""
        new_user = {
            "id": get_next_id(),
            "name": user_data.name,
            "email": user_data.email,
            "role": user_data.role.value,
            "is_active": user_data.is_active
        }
        
        self.db.append(new_user)
        return new_user
    
    def update_user_complete(self, user_id: int, user_data: UserUpdate) -> Dict[str, Any]:
        """Actualización COMPLETA (PUT)"""
        user = self.get_user_by_id(user_id)
        
        user["name"] = user_data.name
        user["email"] = user_data.email
        user["role"] = user_data.role.value
        user["is_active"] = user_data.is_active
        
        return user
    
    def update_user_partial(self, user_id: int, user_data: UserPatch) -> Dict[str, Any]:
        """Actualización PARCIAL (PATCH)"""
        user = self.get_user_by_id(user_id)
        
        update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)
        
        for field, value in update_data.items():
            if field == "role" and value:
                user[field] = value.value
            else:
                user[field] = value
        
        return user
    
    def delete_user(self, user_id: int) -> Dict[str, Any]:
        """Elimina un usuario"""
        user = self.get_user_by_id(user_id)
        self.db.remove(user)
        return {"message": f"Usuario con id {user_id} eliminado exitosamente"}