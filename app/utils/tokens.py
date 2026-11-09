from datetime import datetime, timedelta, timezone
import jwt
from app.config import settings


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