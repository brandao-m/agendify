# REPRESENTA O PROFISSIONAL
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Tenant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

    name: str
    slug: str = Field(index=True, unique=True)

    email: str
    phone: Optional[str] = None
    
    hashed_password: str

    logo_url: str | None = None

    created_at: datetime = Field(default_factory=datetime.utcnow)