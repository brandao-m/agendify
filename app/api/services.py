from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.service import Service
from app.schemas.service import ServiceCreate, ServiceResponse

router = APIRouter(prefix='/services', tags=['Services'])

@router.post('/', response_model=ServiceResponse)
def create_service(data: ServiceCreate, session: Session = Depends(get_session)):

    service = Service(
        tenant_id=data.tenant_id,
        name=data.name,
        duration_minutes=data.duration_minutes,
        price=data.price
    )

    session.add(service)
    session.commit()
    session.refresh(service)

    return service

@router.get('/', response_model=list[ServiceResponse])
def list_services(tenant_id: int, session: Session = Depends(get_session)):

    statement = select(Service).where(Service.tenant_id == tenant_id)

    services = session.exec(statement).all()

    return services