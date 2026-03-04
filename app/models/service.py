# REPRESENTA OS SERVICOS OFERECIDOS
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Service(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tenant_id: int = Field(foreign_key='tenant.id')

    name: str
    duration_minutes: int
    price: Optional[float] = None

    is_active: bool = True

    created_at: datetime = Field(default_factory=datetime.utcnow)