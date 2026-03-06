from pydantic import BaseModel
from datetime import datetime

class CustomerCreate(BaseModel):
    tenant_id: int
    name: str
    phone: str

class CustomerResponse(BaseModel):
    id: int
    tenant_id: int
    name: str
    phone: str
    created_at: datetime