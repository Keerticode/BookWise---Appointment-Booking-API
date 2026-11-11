from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from app.db import database
from app.schemas import availability
from app.services import availability_service
from app.utils import tokens


router = APIRouter(
    prefix = "/availability",
    tags = ["availability"]
)


@router.post("/", status_code = status.HTTP_201_CREATED)
def create_availibility(slot : availability.AvailabilityCreate, db : Session = Depends(database.get_db), current_user = Depends(tokens.get_current_user)) :

    if current_user.role != "provider" :
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail = "Only providers can create availability slots")


    new_slot = availability_service.create_availability_slot(
        db = db,
        service_id = slot.service_id,
        provider_id = current_user.id,
        start_time = slot.start_time,
        end_time = slot.end_time
    )

    return new_slot


@router.get("/")
def get_my_availability(db : Session = Depends(database.get_db), current_user = Depends(tokens.get_current_user)) :

    slots = availability_service.get_availability_slot(db = db, provider_id = current_user.id)

    return slots


@router.get("/public/{service_id}")
def get_public_availability(service_id : int, db : Session = Depends(database.get_db)) :

    slots = availability_service.get_available_slots(db = db, service_id = service_id)

    return slots


@router.put("/{id}")
def update_availability(id: int, slot: availability.AvailabilityUpdate, db: Session = Depends(database.get_db), current_user = Depends(tokens.get_current_user)) :

    if current_user.role != "provider":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only providers can update availability"
        )

    updated_slot = availability_service.update_availability(
        db=db,
        slot_id=id,
        provider_id=current_user.id,
        start_time=slot.start_time,
        end_time=slot.end_time
    )

    return updated_slot


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_availability(id: int, db: Session = Depends(database.get_db), current_user = Depends(tokens.get_current_user)):

    if current_user.role != "provider":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only providers can delete availability"
        )

    availability_service.delete_availability(
        db = db,
        slot_id = id,
        provider_id = current_user.id
    )
