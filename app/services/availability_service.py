from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.services import Service
from app.models.availability import Availabilities


def create_availability_slot(db : Session, service_id : int, provider_id : int, start_time, end_time) :

    existing_service = db.query(Service).filter(Service.id == service_id, Service.provider_id == provider_id).first()

    if existing_service is None :
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Service not found or you dont own this service"
        )

    overlapping_slot = db.query(Availabilities).filter(Availabilities.service_id == service_id, Availabilities.start_time < end_time, Availabilities.end_time > start_time).first()

    if overlapping_slot:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This time slot overlaps with an existing slot")

    new_slot = Availabilities(service_id = service_id, start_time = start_time, end_time = end_time, is_available = True)

    db.add(new_slot)
    db.commit()
    db.refresh(new_slot)

    return new_slot


def get_availability_slot(db : Session, provider_id : int) :

    slots = (
        db.query(Availabilities)
        .join(Service, Availabilities.service_id == Service.id)
        .filter(Service.provider_id == provider_id)
        .all()
    )

    return slots


def get_available_slots(db : Session, service_id : int) :

    slots = db.query(Availabilities).filter(Availabilities.service_id == service_id, Availabilities.is_available == True).all()
    return slots


def update_availability(db: Session, slot_id: int, provider_id: int, start_time, end_time) :

    existing_slot = (
        db.query(Availabilities)
        .join(Service, Availabilities.service_id == Service.id)
        .filter(
            Availabilities.id == slot_id,
            Service.provider_id == provider_id
        )
        .first()
    )

    if existing_slot is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Availability slot not found"
        )

    overlapping_slot = db.query(Availabilities).filter(
        Availabilities.service_id == existing_slot.service_id,
        Availabilities.id != slot_id,
        Availabilities.start_time < end_time,
        Availabilities.end_time > start_time
    ).first()

    if overlapping_slot:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This time slot overlaps with an existing slot"
        )

    existing_slot.start_time = start_time
    existing_slot.end_time = end_time

    db.commit()
    db.refresh(existing_slot)

    return existing_slot


def delete_availability(db: Session, slot_id: int, provider_id: int):

    existing_slot = (
        db.query(Availabilities)
        .join(Service, Availabilities.service_id == Service.id)
        .filter(
            Availabilities.id == slot_id,
            Service.provider_id == provider_id
        )
        .first()
    )

    if existing_slot is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Availability slot not found"
        )

    db.delete(existing_slot)
    db.commit()
