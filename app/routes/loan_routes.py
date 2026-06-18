from fastapi import APIRouter, Depends, status, HTTPException
from typing import Optional
from sqlalchemy.orm import Session

from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services.loan_service import LoanService
from app.dependencies.database_dependency import get_db

router = APIRouter()
loan_service = LoanService()


@router.get(
    "/loans",
    response_model=list[LoanResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar préstamos",
    description="Obtiene la lista de préstamos. Permite filtrar por estado, usuario o dispositivo.",
    response_description="Lista de préstamos",
    tags=["Loans"]
)
def get_loans(
    status_filter: Optional[str] = None,
    user_id:       Optional[int] = None,
    device_id:     Optional[int] = None,
    db: Session = Depends(get_db)
):
    return loan_service.get_all_loans(db, status_filter, user_id, device_id)


@router.get(
    "/loans/details",
    response_model=list[LoanDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar préstamos con información relacionada",
    description="Consulta préstamos usando join() mostrando datos del usuario y del dispositivo. Permite filtrar por estado, email de usuario o tipo de dispositivo.",
    response_description="Lista de préstamos con detalle de usuario y dispositivo",
    tags=["Loans"]
)
def get_loans_details(
    status_filter: Optional[str] = None,
    user_email:    Optional[str] = None,
    device_type:   Optional[str] = None,
    db: Session = Depends(get_db)
):
    return loan_service.get_loans_with_details(db, status_filter, user_email, device_type)


@router.get(
    "/loans/{loan_id}",
    response_model=LoanResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener préstamo por ID",
    description="Retorna los datos de un préstamo específico.",
    response_description="Préstamo encontrado",
    tags=["Loans"]
)
def get_loan(loan_id: int, db: Session = Depends(get_db)):
    loan = loan_service.get_loan_by_id(db, loan_id)
    if not loan:
        raise HTTPException(status_code=404, detail=f"Préstamo con ID {loan_id} no encontrado")
    return loan


@router.post(
    "/loans",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Crear préstamo",
    description="Registra un nuevo préstamo. Valida que el usuario y el dispositivo existan, y que el dispositivo esté disponible.",
    response_description="Préstamo creado",
    tags=["Loans"]
)
def create_loan(loan: LoanCreate, db: Session = Depends(get_db)):
    return loan_service.create_loan(db, loan)


@router.patch(
    "/loans/{loan_id}/return",
    response_model=LoanResponse,
    status_code=status.HTTP_200_OK,
    summary="Devolver dispositivo",
    description="Marca un préstamo como devuelto, asigna fecha de devolución y libera el dispositivo.",
    response_description="Préstamo devuelto",
    tags=["Loans"]
)
def return_loan(loan_id: int, db: Session = Depends(get_db)):
    return loan_service.return_loan(db, loan_id)


@router.get(
    "/users/{user_id}/loans",
    response_model=list[LoanDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar préstamos de un usuario",
    description="Lista todos los préstamos asociados a un usuario específico, con información del dispositivo.",
    response_description="Préstamos del usuario",
    tags=["Loans"]
)
def get_user_loans(user_id: int, db: Session = Depends(get_db)):
    return loan_service.get_loans_by_user(db, user_id)


@router.get(
    "/devices/{device_id}/loans",
    response_model=list[LoanDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar historial de préstamos de un dispositivo",
    description="Lista todos los préstamos asociados a un dispositivo específico, con información del usuario.",
    response_description="Préstamos del dispositivo",
    tags=["Loans"]
)
def get_device_loans(device_id: int, db: Session = Depends(get_db)):
    return loan_service.get_loans_by_device(db, device_id)