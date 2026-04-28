from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.schemas.customer import CustomerCreate, CustomerRead, CustomerUpdate, CustomerDelete

def create_customer(db: Session, customer: CustomerCreate) -> Customer:
    db_customer = Customer(**customer.model_dump())
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    return db_customer

def get_customer(db: Session, customer_id: int) -> Customer | None:
    return db.query(Customer).filter(Customer.id == customer_id).first()


def get_customers(db: Session, skip: int = 0, limit: int = 100) -> list[Customer]:
    return db.query(Customer).offset(skip).limit(limit).all()


def update_customer(db: Session, customer: Customer, customer_update: CustomerUpdate) -> Customer:
    for key, value in customer_update.model_dump().items():
        setattr(customer, key, value)
    db.commit()
    db.refresh(customer)
    return customer

def delete_customer(db: Session, customer: Customer) -> None:
    db.delete(customer)
    db.commit()
    
