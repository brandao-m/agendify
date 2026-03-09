from fastapi import APIRouter, Depends, HTTPException
from datetime import timedelta, datetime, date
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.appointment import Appointment
from app.models.service import Service
from app.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentReschedule

router = APIRouter(prefix='/appointments', tags=['Appointments'])

@router.post('/', response_model=AppointmentResponse)
def create_appointment(
    data: AppointmentCreate,
    session: Session = Depends(get_session)
):
    
    service = session.get(Service, data.service_id)

    if not service:
        return {'error': 'Serviço não encontrado'}
    
    end_at = data.start_at + timedelta(minutes=service.duration_minutes)

    statement = select(Appointment).where(
        Appointment.tenant_id == data.tenant_id,
        Appointment.start_at < end_at,
        Appointment.end_at > data.start_at
    )

    existing = session.exec(statement).first()

    if existing:
        
        raise HTTPException(
            status_code=400,
            detail="Horário já reservado"
        )
    
    appointment = Appointment(
        tenant_id=data.tenant_id,
        customer_id=data.customer_id,
        service_id=data.service_id,
        start_at=data.start_at,
        end_at=end_at,
        status='marcado'
    )

    session.add(appointment)
    session.commit()
    session.refresh(appointment)

    return appointment

@router.get('/day')
def get_day_appointments(
    tenant_id: int,
    appointment_date: date,
    session: Session = Depends(get_session)
):
    
    start_day = datetime.combine(appointment_date, datetime.min.time())
    end_day = datetime.combine(appointment_date, datetime.max.time())

    statement = select(Appointment).where(
        Appointment.tenant_id == tenant_id,
        Appointment.start_at >= start_day,
        Appointment.start_at <= end_day
    ).order_by(Appointment.start_at)

    appointments = session.exec(statement).all()

    return appointments

@router.get('/week')
def get_week_appointments(
        tenant_id: int,
        start_date: date,
        session: Session = Depends(get_session)
):
    
    start_week = datetime.combine(start_date, datetime.min.time())
    end_week = start_week + timedelta(days=7)

    statement = select(Appointment).where(
        Appointment.tenant_id == tenant_id,
        Appointment.start_at >= start_week,
        Appointment.start_at < end_week
    ).order_by(Appointment.start_at)

    appointments = session.exec(statement).all()

    return appointments

@router.patch('/{appointment_id}/cancel')
def cancel_appointment(
    appointment_id: int,
    session: Session = Depends(get_session)
):
    
    appointment = session.get(Appointment, appointment_id)

    if not appointment:
        return {'error': 'Agendamento não encontrado'}
    
    appointment.status = 'cancelado'

    session.add(appointment)
    session.commit()
    session.refresh(appointment)

    return appointment

@router.patch('/{appointment_id}/reschedule')
def reschedule_appointment(
    appointment_id: int,
    data: AppointmentReschedule,
    session: Session = Depends(get_session)
):
    
    appointment = session.get(Appointment, appointment_id)

    if not appointment:
        return {'error': 'Agendamento não encontrado'}
    
    service = session.get(Service, appointment.service_id)

    new_start = data.start_at
    new_end = new_start + timedelta(minutes=service.duration_minutes)

    statement = select(Appointment).where(
        Appointment.tenant_id == appointment.tenant_id,
        Appointment.start_at < new_end,
        Appointment.end_at > new_start,
        Appointment.id != appointment_id
    )

    conflict = session.exec(statement).first()

    if conflict:
        return {'error': 'Horário já reservado'}
    
    appointment.start_at = new_start
    appointment.end_at = new_end
    appointment.status = 'marcado'

    session.add(appointment)
    session.commit()
    session.refresh(appointment)

    return appointment
