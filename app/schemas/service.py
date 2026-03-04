from pydantic import BaseModel

class ServiceCreate(BaseModel):
    tenant_id: int
    name: str
    duration_minutes: int
    price: float | None = None

class ServiceResponse(BaseModel):
    id: int
    tenant_id: int
    name: str
    duration_minutes: int
    price: float | None = None
    is_active: bool