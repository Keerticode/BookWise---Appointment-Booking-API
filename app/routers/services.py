from fastapi import(
    Response,
    status,
    HTTPException,
    Depends,
    APIRouter
)

from app.schemas import services
from app.models.services import Service
from sqlalchemy.orm import Session
from app.db import database
from app.utils import tokens
from typing import List

router = APIRouter(
    prefix="/services",
    tags = ["services"]
)


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = services.serviceOut)
def create_service(service : services.serviceCreate, db : Session = Depends(database.get_db), current_user = Depends(tokens.get_current_user)) :

    if current_user.role != "provider" : 
        raise HTTPException(status_code =status.HTTP_403_FORBIDDEN, detail = "You don't have permission to create a service")

    new_service = Service(provider_id = current_user.id, **service.model_dump())

    db.add(new_service)
    db.commit()
    db.refresh(new_service)

    return new_service


@router.get("/public", response_model=List[services.serviceOut])
def get_all_services(db: Session = Depends(database.get_db)):

    service_list = db.query(Service).all()

    return service_list


@router.get("/", response_model = List[services.serviceOut])
def get_services(db : Session = Depends(database.get_db), current_user = Depends(tokens.get_current_user)) :

    service_list = db.query(Service).filter(Service.provider_id == current_user.id).all()

    return service_list


@router.get("/{id}", response_model = services.serviceOut)
def get_single_service(id : int, db : Session = Depends(database.get_db), current_user = Depends(tokens.get_current_user)) :

    service = db.query(Service).filter(Service.id == id, Service.provider_id == current_user.id).first()

    if not service :
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = f"service with id : {id} not found"
        )

    return service


@router.put("/{id}", response_model=services.serviceOut)
def update_service(id: int,service: services.serviceCreate,db: Session = Depends(database.get_db),current_user=Depends(tokens.get_current_user)):

    existing_service = (db.query(Service).filter(Service.id == id,Service.provider_id == current_user.id).first())

    if existing_service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service with id: {id} doesn't exist"
        )

    update_data = service.model_dump()

    for key, value in update_data.items():
        setattr(existing_service, key, value)

    db.commit()
    db.refresh(existing_service)

    return existing_service


@router.delete("/{id}", status_code = status.HTTP_200_OK)
def delete_service(id : int, db : Session = Depends(database.get_db), current_user = Depends(tokens.get_current_user)) :

    existing_service = db.query(Service).filter(Service.id == id, Service.provider_id == current_user.id).first()

    if existing_service is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Service with id: {id} doesn't exist"
        )

    db.delete(existing_service)
    db.commit()

    return {"message" : "Service deleted successfully"}
