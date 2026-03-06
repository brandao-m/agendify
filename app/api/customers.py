from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.session import get_session
from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerResponse

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
    