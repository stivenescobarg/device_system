from sqlalchemy.orm import Session
from sqlalchemy import asc
from typing import List, Optional
from fastapi import HTTPException, status

from app.models.user_model import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch


class UserService:

    def get_all_users(
        self,
        db: Session,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        order_by: Optional[str] = None
    ) -> List[User]:
        query = db.query(User)

        if role:
            query = query.filter(User.role == role)
        if is_active is not None:
            query = query.filter(User.is_active == is_active)
        if order_by == "name":
            query = query.order_by(asc(User.name))
        elif order_by == "created_at":
            query = query.order_by(asc(User.created_at))

        return query.all()

    def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        return db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create_user(self, db: Session, user_data: UserCreate) -> User:
        if self.get_user_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El email {user_data.email} ya está registrado"
            )

        new_user = User(
            name      = user_data.name,
            email     = user_data.email,
            role      = user_data.role.value,
            is_active = user_data.is_active
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def update_user_complete(self, db: Session, user_id: int, user_data: UserUpdate) -> User:
        user = self.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )

        existing = self.get_user_by_email(db, user_data.email)
        if existing and existing.id != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El email {user_data.email} ya está registrado por otro usuario"
            )

        user.name      = user_data.name
        user.email     = user_data.email
        user.role      = user_data.role.value
        user.is_active = user_data.is_active

        db.commit()
        db.refresh(user)
        return user

    def update_user_partial(self, db: Session, user_id: int, user_data: UserPatch) -> User:
        user = self.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )

        update_data = user_data.model_dump(exclude_unset=True, exclude_none=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se envió ningún campo para actualizar"
            )

        if "email" in update_data:
            existing = self.get_user_by_email(db, update_data["email"])
            if existing and existing.id != user_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El email {update_data['email']} ya está registrado por otro usuario"
                )

        for field, value in update_data.items():
            if field == "role":
                setattr(user, field, value.value if hasattr(value, "value") else value)
            else:
                setattr(user, field, value)

        db.commit()
        db.refresh(user)
        return user

    def delete_user(self, db: Session, user_id: int) -> dict:
        user = self.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {user_id} no encontrado"
            )

        db.delete(user)
        db.commit()
        return {"message": f"Usuario con ID {user_id} eliminado exitosamente"}