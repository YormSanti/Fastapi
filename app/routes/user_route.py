from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.roles import (
    ASSIGN_ROLES,
    CHANGE_ANY_PASSWORD_ROLES,
    CHANGE_OWN_PASSWORD_ROLES,
    MANAGE_USERS_ROLES,
)
from app.core.security import verify_password
from app.dependencies import get_current_user, get_db, require_roles
from app.schemas.user import (
    AdminPasswordChange,
    PasswordChange,
    RoleUpdate,
    UserCreate,
    UserRead,
    UserUpdate,
)
from app.services import user_service


router = APIRouter(
    prefix="/api/users",
    tags=["users"],
)


def get_user_or_404(db: Session, user_id: int):
    user = user_service.get_user(db, user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*MANAGE_USERS_ROLES)),
):
    existing_user = user_service.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )
    return user_service.create_user(db, user)


@router.get("", response_model=list[UserRead])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*MANAGE_USERS_ROLES)),
):
    return user_service.get_users(db, skip=skip, limit=limit)


@router.get("/{user_id}", response_model=UserRead)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*MANAGE_USERS_ROLES)),
):
    user = get_user_or_404(db, user_id)
    return user

@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*MANAGE_USERS_ROLES)),
):
    user = get_user_or_404(db, user_id)
    return user_service.update_user(db, user, user_update
)
    
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*MANAGE_USERS_ROLES)),
):
    user = get_user_or_404(db, user_id)
    user_service.delete_user(db, user)
    return None


@router.patch("/me/password", response_model=UserRead)
def change_own_password(
    password_change: PasswordChange,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*CHANGE_OWN_PASSWORD_ROLES)),
):
    user = get_user_or_404(db, current_user["user_id"])
    if not verify_password(password_change.current_password, user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Current password is incorrect",
        )
    return user_service.update_user_password(db, user, password_change.new_password)


@router.patch("/{user_id}/role", response_model=UserRead)
def assign_role(
    user_id: int,
    role_update: RoleUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*ASSIGN_ROLES)),
):
    user = get_user_or_404(db, user_id)
    return user_service.update_user_role(db, user, role_update.role.value)


@router.patch("/{user_id}/password", response_model=UserRead)
def change_any_password(
    user_id: int,
    password_change: AdminPasswordChange,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*CHANGE_ANY_PASSWORD_ROLES)),
):
    user = get_user_or_404(db, user_id)
    return user_service.update_user_password(db, user, password_change.new_password)


@router.patch("/{user_id}/reset-password", response_model=UserRead)
def reset_password_by_admin(
    user_id: int,
    password_change: AdminPasswordChange,
    db: Session = Depends(get_db),
    current_user: dict = Depends(require_roles(*CHANGE_ANY_PASSWORD_ROLES)),
):
    user = get_user_or_404(db, user_id)
    return user_service.update_user_password(db, user, password_change.new_password)
