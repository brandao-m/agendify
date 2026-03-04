from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Appointment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tenant_id: int = Field(foreign_key='tenant.id')
    customer_id: int = Field(foreign_key='customer.id')
    service_id: int = Field(foreign_key='service.id')

    start_at: datetime
    end_at: datetime

    status: str = 'CONFIRMED'

    created_at: datetime = Field(default_factory=datetime.utcnow)