from pydantic import BaseModel
from datetime import datetime

class AppointmentCreate(BaseModel):

    tenant_id: int
    customer_id: int
    service_id: int
    start_at: datetime

class AppointmentResponse(BaseModel):

    id: int
    tenant_id: int
    customer_id: int
    service_id: int
    start_at: datetime
    end_at: datetime
    status: str

class AppointmentListResponse(BaseModel):

    id: int
    customer_id: int
    service_id: int
    start_at: datetime
    end_at: datetime
    status: str

class AppointmentStatusUpdate(BaseModel):

    status: str

class AppointmentReschedule(BaseModel):

    start_at: datetime