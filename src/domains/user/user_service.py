from typing import List, Optional
from sqlalchemy.orm import Session

from src.domains.user.repository.user_repository import UserRepository
from src.domains.user.models.user_schema import UserCreate, UserUpdate, UserResponse


class UserService:
    def __init__(self, db: Session):
        self.repository = UserRepository(db)

    def get_users(self, skip: int = 0, limit: int = 100) -> List[UserResponse]:
        users = self.repository.get_users(skip, limit)
        return [UserResponse.model_validate(user) for user in users]

    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        user = self.repository.get_user_by_id(user_id)
        if not user:
            return None
        return UserResponse.model_validate(user)

    def create_user(self, user_data: UserCreate) -> UserResponse:
        # dummy check
        if self.repository.get_user_by_email(user_data.email):
            raise ValueError(f"User with email {user_data.email} already exists")

        if self.repository.get_user_by_username(user_data.username):
            raise ValueError(f"User with username {user_data.username} already exists")

        # User erstellen
        user = self.repository.create_user(user_data)
        return UserResponse.model_validate(user)

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        # E-Mail-Kollision prüfen, falls E-Mail aktualisiert wird
        if user_data.email is not None:
            existing_user = self.repository.get_user_by_email(user_data.email)
            if existing_user and existing_user.id != user_id:
                raise ValueError(f"User with email {user_data.email} already exists")

        # Benutzernamen-Kollision prüfen, falls Benutzername aktualisiert wird
        if user_data.username is not None:
            existing_user = self.repository.get_user_by_username(user_data.username)
            if existing_user and existing_user.id != user_id:
                raise ValueError(f"User with username {user_data.username} already exists")

        # User aktualisieren
        updated_user = self.repository.update_user(user_id, user_data)
        if not updated_user:
            return None

        return UserResponse.model_validate(updated_user)

    def delete_user(self, user_id: int) -> bool:
        return self.repository.delete_user(user_id)
