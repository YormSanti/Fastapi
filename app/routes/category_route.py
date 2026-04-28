from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies import get_current_user, get_db
from app.schemas.category import CategoryCreate, CategoryRead, CategoryUpdate, CategoryDelete
from app.services import category_service
 

router = APIRouter(prefix="/api/category", tags=["categories"], dependencies=[Depends(get_current_user)])

@router.post("", response_model=CategoryRead, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    return category_service.create_category(db, category)

@router.get("", response_model=list[CategoryRead])
def read_category(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return category_service.get_categories(db, skip=skip, limit=limit)

@router.get("/{category_id}", response_model=CategoryRead)
def read_category(category_id: int, db: Session = Depends(get_db)):
    category = category_service.get_category(db, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category


@router.put("/{category_id}", response_model=CategoryRead)
def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    db: Session = Depends(get_db),
):
    category = category_service.get_category(db, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    return category_service.update_category(db, category, category_update)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = category_service.get_category(db, category_id)
    if category is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Category not found",
        )
    category_service.delete_category(db, category)
    return None
