from sqlalchemy.orm import Session

from app.models.order import Order
from app.schemas.order import OrderCreate, OrderUpdate

def create_order(db: Session, order: OrderCreate, user_id: int) -> Order:
    db_order = Order(**order.model_dump(), user_id=user_id)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_order(db: Session, order_id: int) -> Order | None:
    return db.query(Order).filter(Order.order_id == order_id).first()

def get_orders(db: Session, skip: int = 0, limit: int = 100) -> list[Order]:
    return db.query(Order).offset(skip).limit(limit).all()


def get_orders_by_user(
    db: Session,
    user_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[Order]:
    return (
        db.query(Order)
        .filter(Order.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

def update_order(db: Session, order: Order, order_update: OrderUpdate) -> Order:
    for key, value in order_update.model_dump().items():
        setattr(order, key, value)
    db.commit()
    db.refresh(order)
    return order

def delete_order(db: Session, order: Order) -> None:
    db.delete(order)
    db.commit()
