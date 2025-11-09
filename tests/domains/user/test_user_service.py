import pytest

from src.domains.user.models.user_schema import UserCreate, UserUpdate


class TestUserService:

    def test_get_users_empty(self, user_service):
        """Test: Leere Liste zurückgeben, wenn keine Benutzer vorhanden sind"""
        users = user_service.get_users()
        assert len(users) == 0

    def test_create_user(self, user_service):
        """Test: Benutzer erstellen"""
        user_data = UserCreate(
            username="newuser",
            email="new@example.com",
            password="password123",
            first_name="New",
            last_name="User"
        )

        user = user_service.create_user(user_data)

        assert user.username == "newuser"
        assert user.email == "new@example.com"
        assert user.first_name == "New"
        assert user.last_name == "User"
        assert user.id is not None

    def test_get_user_by_id(self, user_service, sample_user):
        """Test: Benutzer nach ID abrufen"""
        user = user_service.get_user_by_id(sample_user.id)

        assert user is not None
        assert user.username == sample_user.username
        assert user.email == sample_user.email

    def test_get_user_by_id_not_found(self, user_service):
        """Test: None zurückgeben, wenn Benutzer nicht gefunden wurde"""
        user = user_service.get_user_by_id(999)
        assert user is None

    def test_update_user(self, user_service, sample_user):
        """Test: Benutzer aktualisieren"""
        update_data = UserUpdate(
            first_name="Updated",
            last_name="Name"
        )

        updated_user = user_service.update_user(sample_user.id, update_data)

        assert updated_user is not None
        assert updated_user.first_name == "Updated"
        assert updated_user.last_name == "Name"
        # Unveränderte Felder sollten gleich bleiben
        assert updated_user.username == sample_user.username
        assert updated_user.email == sample_user.email

    def test_delete_user(self, user_service, sample_user):
        """Test: Benutzer löschen"""
        result = user_service.delete_user(sample_user.id)
        assert result is True

        # Überprüfen, dass der Benutzer wirklich gelöscht wurde
        user = user_service.get_user_by_id(sample_user.id)
        assert user is None

    def test_duplicate_email_raises_error(self, user_service, sample_user):
        """Test: Fehler bei doppelter E-Mail-Adresse"""
        user_data = UserCreate(
            username="anotheruser",
            email=sample_user.email,  # Gleiche E-Mail wie sample_user
            password="password123"
        )

        with pytest.raises(ValueError) as excinfo:
            user_service.create_user(user_data)

        assert "already exists" in str(excinfo.value)

    def test_duplicate_username_raises_error(self, user_service, sample_user):
        """Test: Fehler bei doppeltem Benutzernamen"""
        user_data = UserCreate(
            username=sample_user.username,  # Gleicher Benutzername wie sample_user
            email="different@example.com",
            password="password123"
        )

        with pytest.raises(ValueError) as excinfo:
            user_service.create_user(user_data)

        assert "already exists" in str(excinfo.value)
