from fastapi import FastAPI, APIRouter, Response, HTTPException, Depends, status
from app.schemas.users import UserCreate, UserOut
from app.models.users import User
from sqlalchemy.orm import Session
from app.db.database import engine, get_db
from app.utils import hash


router = APIRouter(
    prefix="/users",
    tags = ["Users"]
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model = UserOut)
async def register_user(user : UserCreate, db : Session = Depends(get_db)) :
        
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user :
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT, 
            detail = "Email already registered"
        )
    
    #hashed passwoord - user.password
    hashed_password = hash(user.password)
    user.password = hashed_password
    
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user