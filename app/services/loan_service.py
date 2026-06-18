from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from typing import List, Optional
from datetime import datetime
from fastapi import HTTPException, status

from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate


class LoanService:

    # ── Consultas ──────────────────────────────────────────────────────────────

    def get_all_loans(
        self,
        db: Session,
        status_filter: Optional[str] = None,
        user_id: Optional[int] = None,
        device_id: Optional[int] = None
    ) -> List[Loan]:
        query = db.query(Loan)

        if status_filter:
            query = query.filter(Loan.status == status_filter)
        if user_id:
            query = query.filter(Loan.user_id == user_id)
        if device_id:
            query = query.filter(Loan.device_id == device_id)

        return query.all()

    def get_loan_by_id(self, db: Session, loan_id: int) -> Optional[Loan]:
        return db.query(Loan).filter(Loan.id == loan_id).first()

    # ── Consultas con JOIN ───────────────────────────────────────────────────────

    def get_loans_with_details(
        self,
        db: Session,
        status_filter: Optional[str] = None,
        user_email: Optional[str] = None,
        device_type: Optional[str] = None
    ) -> List[Loan]:
        """
        Consulta préstamos con información relacionada de usuario y dispositivo
        usando join() y carga anticipada con joinedload().
        """
        query = (
            db.query(Loan)
            .join(User, Loan.user_id == User.id)
            .join(Device, Loan.device_id == Device.id)
            .options(joinedload(Loan.user), joinedload(Loan.device))
        )

        filters = []
        if status_filter:
            filters.append(Loan.status == status_filter)
        if user_email:
            filters.append(User.email.ilike(f"%{user_email}%"))
        if device_type:
            filters.append(Device.device_type == device_type)

        if filters:
            query = query.filter(and_(*filters))

        return query.all()

    def get_loans_by_user(self, db: Session, user_id: int) -> List[Loan]:
        return (
            db.query(Loan)
            .filter(Loan.user_id == user_id)
            .options(joinedload(Loan.user), joinedload(Loan.device))
            .all()
        )

    def get_loans_by_device(self, db: Session, device_id: int) -> List[Loan]:
        return (
            db.query(Loan)
            .filter(Loan.device_id == device_id)
            .options(joinedload(Loan.user), joinedload(Loan.device))
            .all()
        )

    # ── Crear préstamo ───────────────────────────────────────────────────────────

    def create_loan(self, db: Session, loan_data: LoanCreate) -> Loan:
        user = db.query(User).filter(User.id == loan_data.user_id).first()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Usuario con ID {loan_data.user_id} no encontrado"
            )

        device = db.query(Device).filter(Device.id == loan_data.device_id).first()
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dispositivo con ID {loan_data.device_id} no encontrado"
            )

        if not device.is_available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El dispositivo '{device.name}' no está disponible para préstamo"
            )

        new_loan = Loan(
            user_id   = loan_data.user_id,
            device_id = loan_data.device_id,
            loan_date = datetime.utcnow(),
            status    = "active"
        )

        device.is_available = False

        db.add(new_loan)
        db.commit()
        db.refresh(new_loan)
        return new_loan

    # ── Devolver dispositivo ─────────────────────────────────────────────────────

    def return_loan(self, db: Session, loan_id: int) -> Loan:
        loan = self.get_loan_by_id(db, loan_id)
        if not loan:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Préstamo con ID {loan_id} no encontrado"
            )

        if loan.status == "returned":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"El préstamo con ID {loan_id} ya fue devuelto"
            )

        loan.status      = "returned"
        loan.return_date = datetime.utcnow()

        device = db.query(Device).filter(Device.id == loan.device_id).first()
        if device:
            device.is_available = True

        db.commit()
        db.refresh(loan)
        return loan