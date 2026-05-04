from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate, CustomerDelete
from app.services import customer_service


router = APIRouter(
    prefix="/api/customers",
    tags=["customers"],
    dependencies=[Depends(get_current_user)]
)

@router.post("", response_model=CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer: CustomerCreate,
    db: Session = Depends(get_db),
):
    return customer_service.create_customer(db, customer)

@router.get("", response_model=list[CustomerRead])
def read_customers(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return customer_service.get_customers(db, skip=skip, limit=limit)



@router.get("/{customer_id}", response_model=CustomerRead)
async def read_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = customer_service.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer

@router.put("/{customer_id}", response_model=CustomerRead)
async def update_customer(
    customer_id: int,
    customer_update: CustomerUpdate,
    db: Session = Depends(get_db),
):
    customer = customer_service.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer_service.update_customer(db, customer, customer_update)

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_customer(
    customer_id: int,
    db: Session = Depends(get_db),
):
    customer = customer_service.get_customer(db, customer_id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    customer_service.delete_customer(db, customer)
    return None

