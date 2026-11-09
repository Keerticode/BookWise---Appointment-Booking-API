from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.config import settings
from schemas import users


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