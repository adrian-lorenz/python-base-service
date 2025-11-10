import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from src.backend.database import Base
from src.services.user.models.user_model import User
from src.services.user.repository.user_repository import UserRepository
from src.services.user.user_service import UserService


# In-Memory SQLite-Datenbank für Tests
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture
def test_db_engine():
    """Erstellt eine Test-Datenbankengine mit In-Memory SQLite"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Wichtig für In-Memory SQLite
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_db_session(test_db_engine):
    """Erstellt eine Test-Datenbanksession"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_db_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture
def user_repository(test_db_session):
    """Erstellt ein User-Repository mit Test-Datenbanksession"""
    return UserRepository(test_db_session)


@pytest.fixture
def user_service(test_db_session):
    """Erstellt einen User-Service mit Test-Datenbanksession"""
    return UserService(test_db_session)


@pytest.fixture
def sample_user(user_repository):
    """Erstellt einen Beispiel-Benutzer für Tests"""
    from src.services.user.models.user_schema import UserCreate

    user_data = UserCreate(
        username="testuser",
        email="test@example.com",
        password="password123",
        first_name="Test",
        last_name="User"
    )
    return user_repository.create_user(user_data)
