from enum import Enum
from pydantic import BaseModel, EmailStr


# validates data sent by a client when creating a service
class serviceCreate(BaseModel) :
    name : str = Field(min_length = 3, max_length = 100)
    description : str | None = None
    duration_minutes : int = Field(gt = 0, le = 480)
    price : Decimal = Field(ge = 0, max_digits = 10, decimal_places = 2)


# validates data returned by API
class ServiceOut(BaseModel):
    id: int
    name: str
    description: str | None
    duration_minutes: int
    price: Decimal
    provider_id: int

    model_config = ConfigDict(from_attributes=True)