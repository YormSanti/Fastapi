from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.services import category_service, product_service


router = APIRouter(prefix="/api/products", tags=["products"], dependencies=[Depends(get_current_user)] )


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
):
    if product.category_id is not None and category_service.get_category(db, product.category_id) is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return product_service.create_product(db, product)


@router.get("", response_model=list[ProductRead])
async def read_products(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return product_service.get_products(db, skip=skip, limit=limit)


@router.get("/{product_id}", response_model=ProductRead)
async def read_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product


@router.put("/{product_id}", response_model=ProductRead)
async def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
):
    if (
        product_update.category_id is not None
        and category_service.get_category(db, product_update.category_id) is None
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )

    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product_service.update_product(db, product, product_update)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
):
    product = product_service.get_product(db, product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    await product_service.delete_product(db, product)
    return None
