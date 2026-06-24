from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_model import User
from app.schemas.auth_schema import UserRegister
from app.auth.security import get_password_hash, verify_password, create_access_token


class AuthService:

    def get_user_by_email(self, db: Session, email: str):
        return db.query(User).filter(User.email == email).first()

    def register_user(self, db: Session, user_data: UserRegister) -> User:
        # Verificar email duplicado
        if self.get_user_by_email(db, user_data.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El email {user_data.email} ya está registrado"
            )

        new_user = User(
            name            = user_data.name,
            email           = user_data.email,
            hashed_password = get_password_hash(user_data.password),
            role            = user_data.role,
            is_active       = True
        )

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    def login_user(self, db: Session, email: str, password: str) -> dict:
        user = self.get_user_by_email(db, email)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )

        if not user.hashed_password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Este usuario no tiene contraseña configurada. Regístrese nuevamente."
            )

        if not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email o contraseña incorrectos"
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuario inactivo"
            )

        access_token = create_access_token(
            data={"sub": user.email, "role": user.role}
        )

        return {
            "access_token": access_token,
            "token_type":   "bearer"
        }