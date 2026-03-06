from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from app.db.session import get_session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerFindOrCreate, CustomerResponse

router = APIRouter(prefix='/customers', tags=['Customers'])

@router.post('/', response_model=CustomerResponse)
def create_customer(
    data: CustomerCreate,
    session: Session = Depends(get_session)
):
    
    customer = Customer(
        tenant_id=data.tenant_id,
        name=data.name,
        phone=data.phone
    )

    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer

@router.post('/find-or-create', response_model=CustomerResponse)
def find_or_create_customer(
    data: CustomerFindOrCreate,
    session: Session = Depends(get_session)
):
    
    statement = select(Customer).where(
        Customer.phone == data.phone,
        Customer.tenant_id == data.tenant_id
    )

    customer = session.exec(statement).first()

    if customer:
        return customer
    
    customer = Customer(
        tenant_id=data.tenant_id,
        name=data.name,
        phone=data.phone
    )

    session.add(customer)
    session.commit()
    session.refresh(customer)

    return customer
    