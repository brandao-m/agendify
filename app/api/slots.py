from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.service import Service
from app.models.weekly_availability import WeeklyAvailability
from app.models.appointment import Appointment
from app.utils.slots import generate_slots

router = APIRouter(prefix="/slots", tags=["Slots"])


@router.get("/available")
def get_available_slots(
    tenant_id: int,
    service_id: int,
    appointment_date: date,
    session: Session = Depends(get_session)
):

    # BUSCAR SERVIÇO
    service = session.get(Service, service_id)

    if not service:
        return []

    weekday = appointment_date.weekday()

    # BUSCAR TODAS AS DISPONIBILIDADES DO DIA
    statement = select(WeeklyAvailability).where(
        WeeklyAvailability.tenant_id == tenant_id,
        WeeklyAvailability.weekday == weekday,
        WeeklyAvailability.is_active == True
    )

    availabilities = session.exec(statement).all()

    if not availabilities:
        return []

    # GERAR SLOTS DE TODOS OS PERÍODOS
    slots = []

    for availability in availabilities:

        period_slots = generate_slots(
            availability.start_time,
            availability.end_time,
            service.duration_minutes
        )

        slots.extend(period_slots)

    # INTERVALO DO DIA
    start_day = datetime.combine(appointment_date, datetime.min.time())
    end_day = start_day + timedelta(days=1)

    # BUSCAR AGENDAMENTOS
    statement = select(Appointment).where(
        Appointment.tenant_id == tenant_id,
        Appointment.start_at >= start_day,
        Appointment.start_at < end_day
    )

    appointments = session.exec(statement).all()

    booked_times = [a.start_at.time() for a in appointments]

    # FILTRAR HORÁRIOS OCUPADOS
    available_slots = [s for s in slots if s not in booked_times]

    return available_slots