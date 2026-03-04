from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Customer(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    tenant_id: int = Field(foreign_key='tenant_id')

    name: str
    phone: str

    created_at: datetime = Field(default_factory=datetime.utcnow)