from fastapi import APIRouter, Depends
from datetime import date
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.service import Service
from app.models.weekly_availability import WeeklyAvailability
from app.models.appointment import Appointment
from app.utils.slots import generate_slots

router = APIRouter(prefix='/slots', tags=['Slots'])

@router.get('/available')
def get_available_slots(
    tenant_id: int,
    service_id: int,
    appointment_date: date,
    session: Session = Depends(get_session)
):
    
    # BUSCAR SERVICO
    service = session.get(Service, service_id)

    if not service:
        return {'error': 'Serviço não encontrado'}
    
    weekday = appointment_date.weekday()

    # BUSCAR DISPONIBILIDADE
    statement = select(WeeklyAvailability).where(
        WeeklyAvailability.tenant_id == tenant_id,
        WeeklyAvailability.weekday == weekday,
        WeeklyAvailability.is_active == True
    )

    availability = session.exec(statement).first()

    if not availability:
        return []
    
    # GERAR SLOTS
    slots = generate_slots(
        availability.start_time,
        availability.end_time,
        service.duration_minutes
    )

    # BUSCAR AGENDAMENTOS EXISTENTES
    statement = select(Appointment).where(
        Appointment.tenant_id == tenant_id,
        Appointment.start_at >= appointment_date,
        Appointment.start_at < appointment_date.replace(day=appointment_date.day +1)
    )

    appointments = session.exec(statement).all()

    booked_times = [a.start_at.time() for a in appointments]

    available_slots = [s for s in slots if s not in booked_times]

    return available_slots