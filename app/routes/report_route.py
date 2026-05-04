from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.roles import VIEW_REPORTS_ROLES
from app.dependencies import get_db, require_roles
from app.models.order import Order


router = APIRouter(
    prefix="/api/reports",
    tags=["reports"],
    dependencies=[Depends(require_roles(*VIEW_REPORTS_ROLES))],
)


@router.get("/orders")
def order_report(db: Session = Depends(get_db)):
    total_orders = db.query(func.count(Order.order_id)).scalar() or 0
    total_amount = db.query(func.coalesce(func.sum(Order.total_amount), 0)).scalar() or 0
    return {
        "total_orders": total_orders,
        "total_amount": float(total_amount),
    }
