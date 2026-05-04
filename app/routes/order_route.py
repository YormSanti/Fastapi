from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.roles import (
    CREATE_ORDER_ROLES,
    DELETE_ORDER_ROLES,
    UPDATE_ORDER_ROLES,
    UserRole,
    VIEW_ALL_ORDERS_ROLES,
)
from app.dependencies import get_db, get_current_user, has_role, require_roles
from app.schemas.order import OrderCreate, OrderRead, OrderUpdate
from app.schemas.order_detail import (
    OrderDetailCreate,
    OrderDetailRead,
    OrderDetailUpdate,
)
from app.services import (
    customer_service,
    order_detail_service,
    order_service,
    product_service,
)


router = APIRouter(
    prefix="/api/orders",
    tags=["orders"],
    dependencies=[Depends(get_current_user)],
)

@router.post("", response_model=OrderRead, status_code=status.HTTP_201_CREATED)
async def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*CREATE_ORDER_ROLES)),
):
    if customer_service.get_customer(db, order.customer_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return order_service.create_order(db, order, user_id=current_user["user_id"])


@router.get("", response_model=list[OrderRead])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    if has_role(current_user, *VIEW_ALL_ORDERS_ROLES):
        return order_service.get_orders(db, skip=skip, limit=limit)
    return order_service.get_orders_by_user(
        db,
        user_id=current_user["user_id"],
        skip=skip,
        limit=limit,
    )


@router.get("/{order_id}", response_model=OrderRead)
async def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    order = order_service.get_order(db, order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    if not has_role(current_user, *VIEW_ALL_ORDERS_ROLES) and order.user_id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return order


@router.put("/{order_id}", response_model=OrderRead)
async def update_order(
    order_id: int,
    order_update: OrderUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*UPDATE_ORDER_ROLES)),
):
    if customer_service.get_customer(db, order_update.customer_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )

    order = order_service.get_order(db, order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    return order_service.update_order(db, order, order_update)


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*DELETE_ORDER_ROLES)),
):
    order = order_service.get_order(db, order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    order_service.delete_order(db, order)
    return None


@router.post(
    "/{order_id}/details",
    response_model=OrderDetailRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_order_detail(
    order_id: int,
    order_detail: OrderDetailCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*CREATE_ORDER_ROLES)),
):
    order = order_service.get_order(db, order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    if current_user.get("role") == UserRole.USER.value and order.user_id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    if product_service.get_product(db, order_detail.product_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return order_detail_service.create_order_detail(db, order_id, order_detail)


@router.get("/{order_id}/details", response_model=list[OrderDetailRead])
async def get_order_details(
    order_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    order = order_service.get_order(db, order_id)
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found",
        )
    if not has_role(current_user, *VIEW_ALL_ORDERS_ROLES) and order.user_id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    return order_detail_service.get_order_details(
        db,
        order_id=order_id,
        skip=skip,
        limit=limit,
    )


@router.get(
    "/{order_id}/details/{order_detail_id}",
    response_model=OrderDetailRead,
)
async def get_order_detail(
    order_id: int,
    order_detail_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
):
    order = order_service.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if not has_role(current_user, *VIEW_ALL_ORDERS_ROLES) and order.user_id != current_user["user_id"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    order_detail = order_detail_service.get_order_detail(db, order_detail_id)
    if order_detail is None or order_detail.order_id != order_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order detail not found",
        )
    return order_detail


@router.put(
    "/{order_id}/details/{order_detail_id}",
    response_model=OrderDetailRead,
)
async def update_order_detail(
    order_id: int,
    order_detail_id: int,
    order_detail_update: OrderDetailUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*UPDATE_ORDER_ROLES)),
):
    order_detail = order_detail_service.get_order_detail(db, order_detail_id)
    if order_detail is None or order_detail.order_id != order_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order detail not found",
        )
    if product_service.get_product(db, order_detail_update.product_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return order_detail_service.update_order_detail(
        db,
        order_detail,
        order_detail_update,
    )


@router.delete(
    "/{order_id}/details/{order_detail_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_order_detail(
    order_id: int,
    order_detail_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*DELETE_ORDER_ROLES)),
):
    order_detail = order_detail_service.get_order_detail(db, order_detail_id)
    if order_detail is None or order_detail.order_id != order_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order detail not found",
        )
    order_detail_service.delete_order_detail(db, order_detail)
    return None
