from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password


def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    return db.query(User).offset(skip).limit(limit).all()


def create_user(db: Session, user: UserCreate) -> User:
    db_user = User(
        firstName=user.firstName,
        lastName=user.lastName,
        password=hash_password(user.password),
        email=user.email,
        role=user.role.value,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, db_user: User, user_update: UserUpdate) -> User:
    db_user.firstName = user_update.firstName
    db_user.lastName = user_update.lastName
    db_user.password = hash_password(user_update.password)
    db_user.email = user_update.email
    db_user.role = user_update.role.value
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_role(db: Session, db_user: User, role: str) -> User:
    db_user.role = role
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_password(db: Session, db_user: User, password: str) -> User:
    db_user.password = hash_password(password)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, db_user: User) -> None:
    db.delete(db_user)
    db.commit()
    
