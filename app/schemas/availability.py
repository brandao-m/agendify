from pydantic import BaseModel
from datetime import time

class AvailabilityCreate(BaseModel):
    tenant_id: int
    weekday: int
    start_time: time
    end_time: time
    is_active: bool = True

class AvailabilityResponse(BaseModel):
     id: int
     tenant_id: int
     weekday: int
     start_time: time
     end_time: time
     is_active: bool