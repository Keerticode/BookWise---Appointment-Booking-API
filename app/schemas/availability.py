from datetime import datetime
from pydantic import BaseModel, model_validator


class AvailabilityCreate(BaseModel):
    service_id: int
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_time(self):
        if self.end_time <= self.start_time:
            raise ValueError("End time must be after start time")
        return self