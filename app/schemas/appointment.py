
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, ConfigDict, Field


class AppointmentStatus(str, Enum):
    booked = "booked"
    cancelled = "cancelled"
    completed = "completed"


class AppointmentCreate(BaseModel):
    slot_id: int = Field(gt=0)


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus


class AppointmentOut(BaseModel):
    id: int
    customer_id: int
    slot_id: int
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
