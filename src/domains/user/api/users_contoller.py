from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from src.app.database import get_db
from src.domains.user.user_service import UserService
from src.domains.user.models.user_schema import UserCreate, UserUpdate, UserResponse

# Router für User-Endpunkte erstellen
router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


# Dependency für User-Service
def get_user_service(db: Session = Depends(get_db)):
    return UserService(db)


@router.get("/", response_model=List[UserResponse])
def read_users(
        skip: int = 0,
        limit: int = 100,
        service: UserService = Depends(get_user_service)
):
    """Alle User abrufen"""
    users = service.get_users(skip, limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
        user_id: int,
        service: UserService = Depends(get_user_service)
):
    """Einen User anhand seiner ID abrufen"""
    user = service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return user


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
        user_data: UserCreate,
        service: UserService = Depends(get_user_service)
):
    """Neuen User erstellen"""
    try:
        return service.create_user(user_data)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{user_id}", response_model=UserResponse)
def update_user(
        user_id: int,
        user_data: UserUpdate,
        service: UserService = Depends(get_user_service)
):
    """User aktualisieren"""
    try:
        user = service.update_user(user_id, user_data)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {user_id} not found"
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user_id: int,
        service: UserService = Depends(get_user_service)
):
    """User löschen"""
    result = service.delete_user(user_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found"
        )
    return None


# Export des Routers
UsersController = router
