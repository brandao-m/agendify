from pydantic import BaseModel, EmailStr

class TenantCreate(BaseModel):
    name: str
    slug: str
    email: EmailStr
    phone: str | None = None
    password: str

class TenantResponse(BaseModel):
    id: int
    name: str
    slug: str
    email: str
    phone: str | None = None