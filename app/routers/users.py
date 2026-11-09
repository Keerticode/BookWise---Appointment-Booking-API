from fastapi import FastAPI, APIRouter, Response, HTTPException, Depends, status
from app.schemas.users import UserCreate, UserOut, Token, TokenData, UserLogin
from app.models.users import User
from sqlalchemy.orm import Session
from app.db.database import engine, get_db
from app.utils.password import hash, verify
from app.utils.tokens import create_access_token

router = APIRouter(
    prefix="/users",
    tags = ["Users"]
)


#User's Registration ---->

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


#User's Login ---->

@router.post("/login", response_model = Token)
async def login(user_credentials : UserLogin, db : Session = Depends(get_db)) :

    user = db.query(User).filter(
        User.email == user_credentials.email
    ).first()

    if not user :
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password" 
        )

    if not verify(user_credentials.password, user.password) :
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Invalid email or password"
        )

    access_token = create_access_token(
        data = {"sub" : str(user.id)}
    )

    return {
        "access_token" : access_token,
        "token_type" : "bearer"
    }