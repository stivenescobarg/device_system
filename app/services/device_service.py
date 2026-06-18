from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from fastapi import HTTPException, status
from app.models.loan_model import Loan
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch


class DeviceService:

    def get_all_devices(
        self,
        db: Session,
        device_type: Optional[str] = None,
        is_available: Optional[bool] = None,
        brand: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Device]:
        query = db.query(Device)

        if device_type:
            query = query.filter(Device.device_type == device_type)
        if is_available is not None:
            query = query.filter(Device.is_available == is_available)
        if brand:
            query = query.filter(Device.brand.ilike(f"%{brand}%"))
        if search:
            query = query.filter(
                or_(
                    Device.name.ilike(f"%{search}%"),
                    Device.serial_number.ilike(f"%{search}%")
                )
            )

        return query.all()

    def get_device_by_id(self, db: Session, device_id: int) -> Optional[Device]:
        return db.query(Device).filter(Device.id == device_id).first()

    def get_device_by_serial(self, db: Session, serial_number: str) -> Optional[Device]:
        return db.query(Device).filter(Device.serial_number == serial_number).first()

    def create_device(self, db: Session, device_data: DeviceCreate) -> Device:
        if self.get_device_by_serial(db, device_data.serial_number):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El número de serie {device_data.serial_number} ya está registrado"
            )

        new_device = Device(
            name          = device_data.name,
            serial_number = device_data.serial_number,
            device_type   = device_data.device_type,
            brand         = device_data.brand,
            is_available  = device_data.is_available
        )

        db.add(new_device)
        db.commit()
        db.refresh(new_device)
        return new_device

    def update_device_complete(self, db: Session, device_id: int, device_data: DeviceUpdate) -> Device:
        device = self.get_device_by_id(db, device_id)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dispositivo con ID {device_id} no encontrado"
            )

        existing = self.get_device_by_serial(db, device_data.serial_number)
        if existing and existing.id != device_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El número de serie {device_data.serial_number} ya está registrado por otro dispositivo"
            )

        device.name          = device_data.name
        device.serial_number = device_data.serial_number
        device.device_type   = device_data.device_type
        device.brand         = device_data.brand
        device.is_available  = device_data.is_available

        db.commit()
        db.refresh(device)
        return device

    def update_device_partial(self, db: Session, device_id: int, device_data: DevicePatch) -> Device:
        device = self.get_device_by_id(db, device_id)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dispositivo con ID {device_id} no encontrado"
            )

        update_data = device_data.model_dump(exclude_unset=True, exclude_none=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No se envió ningún campo para actualizar"
            )

        if "serial_number" in update_data:
            existing = self.get_device_by_serial(db, update_data["serial_number"])
            if existing and existing.id != device_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El número de serie {update_data['serial_number']} ya está registrado por otro dispositivo"
                )

        for field, value in update_data.items():
            setattr(device, field, value)

        db.commit()
        db.refresh(device)
        return device

    def delete_device(self, db: Session, device_id: int) -> dict:
        device = self.get_device_by_id(db, device_id)
        if not device:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Dispositivo con ID {device_id} no encontrado"
            )

        active_loan = (
            db.query(Loan)
            .filter(Loan.device_id == device_id, Loan.status == "active")
            .first()
        )
        if active_loan:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"No se puede eliminar el dispositivo con ID {device_id} porque tiene un préstamo activo"
            )

        db.delete(device)
        db.commit()
        return {"message": f"Dispositivo con ID {device_id} eliminado exitosamente"}