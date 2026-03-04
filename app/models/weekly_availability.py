from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import time

class WeeklyAvailability(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tenant_id: int = Field(foreign_key='tenant.id')

    weekday: int
    start_time: time
    end_time: time

    is_active: bool = True