import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.domains.user.api.users_contoller import router, get_user_service


# Test-App erstellen
@pytest.fixture
def app(test_db_session):
    """Test-App mit Override für Dependency Injection"""
    app = FastAPI()

    # Override der Dependency für den User-Service
    def override_get_user_service():
        from src.domains.user.user_service import UserService
        return UserService(test_db_session)

    app.include_router(router)
    app.dependency_overrides[get_user_service] = override_get_user_service

    return app


@pytest.fixture
def client(app):
    """Test-Client für API-Anfragen"""
    return TestClient(app)


@pytest.fixture
def sample_api_user(client):
    """Erstellt einen Beispiel-Benutzer über die API"""
    user_data = {
        "username": "apiuser",
        "email": "api@example.com",
        "password": "password123",
        "first_name": "API",
        "last_name": "User"
    }
    response = client.post("/users/", json=user_data)
    return response.json()


class TestUsersController:

    def test_create_user(self, client):
        """Test: Benutzer über API erstellen"""
        user_data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "password123",
            "first_name": "New",
            "last_name": "User"
        }

        response = client.post("/users/", json=user_data)

        assert response.status_code == 201
        data = response.json()
        assert data["username"] == user_data["username"]
        assert data["email"] == user_data["email"]
        assert "id" in data

    def test_read_users(self, client, sample_api_user):
        """Test: Alle Benutzer abrufen"""
        response = client.get("/users/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    def test_read_user(self, client, sample_api_user):
        """Test: Einzelnen Benutzer abrufen"""
        user_id = sample_api_user["id"]
        response = client.get(f"/users/{user_id}")

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["username"] == sample_api_user["username"]

    def test_read_user_not_found(self, client):
        """Test: 404 bei nicht existierendem Benutzer"""
        response = client.get("/users/999")
        assert response.status_code == 404

    def test_update_user(self, client, sample_api_user):
        """Test: Benutzer aktualisieren"""
        user_id = sample_api_user["id"]
        update_data = {
            "first_name": "Updated",
            "last_name": "Name"
        }

        response = client.put(f"/users/{user_id}", json=update_data)

        assert response.status_code == 200
        data = response.json()
        assert data["id"] == user_id
        assert data["first_name"] == update_data["first_name"]
        assert data["last_name"] == update_data["last_name"]
        assert data["username"] == sample_api_user["username"]  # Unverändert

    def test_delete_user(self, client, sample_api_user):
        """Test: Benutzer löschen"""
        user_id = sample_api_user["id"]

        response = client.delete(f"/users/{user_id}")
        assert response.status_code == 204

        # Überprüfen, dass der Benutzer wirklich gelöscht wurde
        response = client.get(f"/users/{user_id}")
        assert response.status_code == 404
