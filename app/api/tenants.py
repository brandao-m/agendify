from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantResponse
from app.core.security import hash_password

router = APIRouter(prefix='/tenants', tags=['Tenants'])

@router.post('/', response_model=TenantResponse)
def create_tenant(data: TenantCreate, session: Session = Depends(get_session)):

    tenant = Tenant(
        name=data.name,
        slug=data.slug,
        email=data.email,
        phone=data.phone,
        hashed_password=hash_password(data.password)
    )

    session.add(tenant)
    session.commit()
    session.refresh(tenant)

    return tenant

@router.get('/slug/{slug}')
def get_tenant_by_slug(slug: str, session: Session = Depends(get_session)):

    statement= select(Tenant).where(Tenant.slug == slug)

    tenant = session.exec(statement).first()

    return tenant