from sqlalchemy.orm import Session

from app.models.orderDetail import OrderDetail
from app.models.product import Product
from app.schemas.order_detail import OrderDetailCreate, OrderDetailUpdate


def _calculate_subtotal(order_detail: OrderDetailCreate | OrderDetailUpdate) -> float:
    discount_amount = order_detail.discount_amount or 0
    return (order_detail.qty * order_detail.price) - discount_amount


def create_order_detail(
    db: Session,
    order_id: int,
    order_detail: OrderDetailCreate,
) -> OrderDetail:
    product = db.query(Product).filter(Product.id == order_detail.product_id).first()
    db_order_detail = OrderDetail(
        **order_detail.model_dump(),
        order_id=order_id,
        product_name=product.productName if product else "",
        subtotal=_calculate_subtotal(order_detail),
    )
    db.add(db_order_detail)
    db.commit()
    db.refresh(db_order_detail)
    return db_order_detail


def get_order_detail(db: Session, order_detail_id: int) -> OrderDetail | None:
    return (
        db.query(OrderDetail)
        .filter(OrderDetail.OrderDetail_id == order_detail_id)
        .first()
    )


def get_order_details(
    db: Session,
    order_id: int,
    skip: int = 0,
    limit: int = 100,
) -> list[OrderDetail]:
    return (
        db.query(OrderDetail)
        .filter(OrderDetail.order_id == order_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_order_detail(
    db: Session,
    order_detail: OrderDetail,
    order_detail_update: OrderDetailUpdate,
) -> OrderDetail:
    product = db.query(Product).filter(Product.id == order_detail_update.product_id).first()
    update_data = order_detail_update.model_dump()
    for key, value in update_data.items():
        setattr(order_detail, key, value)

    order_detail.product_name = product.productName if product else ""
    order_detail.subtotal = _calculate_subtotal(order_detail_update)
    db.commit()
    db.refresh(order_detail)
    return order_detail


def delete_order_detail(db: Session, order_detail: OrderDetail) -> None:
    db.delete(order_detail)
    db.commit()
