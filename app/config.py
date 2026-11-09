#Pydantic is the most widely used data validation and data parsing library fro python, ensuring that incoming data (like API payloads, configuration files, or database results) is valid, safely type-coerced, and correctly structured at runtime

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings) :
    sqlalchemy_database_url: str

    jwt_secret_key : str
    jwt_algorithm : str = "HS256"
    access_token_expire_minutes : int = 30

    model_config = SettingsConfigDict(
        env_file = ".env",
        extra = "ignore"
    )

settings = Settings()