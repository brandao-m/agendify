from sqlmodel import SQLModel
from app.db.session import engine
from app.models import *

# IMPORTAR OS MODELS
from app.models.tenant import Tenant
from app.models.service import Service
from app.models.weekly_availability import WeeklyAvailability
from app.models.customer import Customer
from app.models.appointment import Appointment

def init_db():
    SQLModel.metadata.create_all(engine)