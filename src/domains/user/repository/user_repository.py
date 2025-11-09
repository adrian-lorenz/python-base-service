from typing import Optional
from sqlalchemy.orm import Session

from src.domains.user.models.user_model import User
from src.domains.user.models.user_schema import UserCreate, UserUpdate


class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_users(self, skip: int = 0, limit: int = 100) -> list[type[User]]:
        return self.db.query(User).offset(skip).limit(limit).all()

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def get_user_by_username(self, username: str) -> Optional[User]:
        return self.db.query(User).filter(User.username == username).first()

    def create_user(self, user: UserCreate) -> User:

        hashed_password = user.password + "_hashed"  # demo

        db_user = User(
            username=user.username,
            email=user.email,
            hashed_password=hashed_password,
            first_name=user.first_name,
            last_name=user.last_name,
            is_active=user.is_active
        )
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[User]:
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return None

        # Aktualisiere nur die angegebenen Felder
        user_data_dict = user_data.model_dump(exclude_unset=True)

        # Passwort separat behandeln, falls vorhanden
        if "password" in user_data_dict:
            user_data_dict["hashed_password"] = user_data_dict.pop("password") + "_hashed"

        for key, value in user_data_dict.items():
            setattr(db_user, key, value)

        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def delete_user(self, user_id: int) -> bool:
        db_user = self.get_user_by_id(user_id)
        if not db_user:
            return False

        self.db.delete(db_user)
        self.db.commit()
        return True
