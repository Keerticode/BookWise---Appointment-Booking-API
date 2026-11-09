from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.config import settings
from app.schemas import users
from fastapi.security import OAuth2PasswordBearer
from fastapi import status, HTTPException, Depends
from app.db import database
from sqlalchemy.orm import Session
from app.models import users

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = "login")

SECRET_KEY = settings.jwt_secret_key
ALGORITHM = settings.jwt_algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data : dict) :
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(
        minutes = settings.access_token_expire_minutes
    )

    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm = settings.jwt_algorithm
    )

    return encoded_jwt


def verify_access_token(token : str, credentials_exception) : 

    try :
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms = [settings.jwt_algorithm])

        id : str = payload.get("user_id")

        if id is None :
            raise credentials_exception
        token_data = users.TokenData(id = id)

    except JWTError :

        raise credentials_exception

    return token_data


def get_current_user(token : str = Depends(oauth2_scheme), db : Session = Depends(database.get_db)) :

    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers = {"WWW-Authentication" : "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(users.User).filter(models.User.id == token.id).first()

    return user