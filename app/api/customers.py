from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError

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
    
    # PROCURA SE O CLIENTE EXISTE
    statement = select(Customer).where(Customer.phone == data.phone)
    customer = session.exec(statement).first()

    if customer:
        return customer
    
    # TENTA CRIAR CLIENTE
    customer = Customer(
        tenant_id=data.tenant_id,
        name=data.name,
        phone=data.phone
    )

    session.add(customer)

    try:
        session.commit()
        session.refresh(customer)
        return customer
    
    except IntegrityError:

        session.rollback()

        # SE HOUVE DUPLICAÇÃO, BUSCA NOVAMENTE
        statement = select(Customer).where(Customer.phone == data.phone)
        customer = session.exec(statement).first()

        return customer
    
@router.get('/')
def list_customers(
    tenant_id: int,
    session: Session = Depends(get_session)
):
        
    statement = select(Customer).where(
    Customer.tenant_id == tenant_id
    ).order_by(Customer.created_at.desc())

    customers = session.exec(statement).all()

    return customers

    