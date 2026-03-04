from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.weekly_availability import WeeklyAvailability
from app.schemas.availability import AvailabilityCreate, AvailabilityResponse

router = APIRouter(prefix='/availability', tags=['Availability'])

@router.post('/', response_model=AvailabilityResponse)
def create_availability(
    data: AvailabilityCreate,
    session: Session = Depends(get_session)
):
    availability = WeeklyAvailability(
        tenant_id=data.tenant_id,
        weekday=data.weekday,
        start_time=data.start_time,
        end_time=data.end_time,
        is_active=data.is_active
    )

    session.add(availability)
    session.commit()
    session.refresh(availability)

    return availability

@router.get('/', response_model=list[AvailabilityResponse])
def list_availability(
    tenant_id: int,
    session: Session = Depends(get_session)
):
    statement = select(WeeklyAvailability).where(
        WeeklyAvailability.tenant_id == tenant_id
    )

    result = session.exec(statement).all()

    return result