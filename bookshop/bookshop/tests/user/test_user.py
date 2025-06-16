import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from tests.factories import UserFactory


@pytest.mark.django_db
class TestsUser:
    endpoint_registration = "/api/registration/"
    endpoint_login = "/api/drf-auth/login/"

    def test_create_user(self, api_client, user_data):
        expected_json = user_data
        response = api_client.post(
            self.endpoint_registration, data=expected_json, format="json"
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert get_user_model().objects.filter(username="testuser").exists()

    def test_user_can_login(self, api_client):
        password = "testpassword"
        user = UserFactory(password=password)
        response = api_client.post(
            self.endpoint_login, {"username": user.username, "password": password}
        )
        assert response.status_code == status.HTTP_200_OK

    def test_user_can_be_deleted1(self, api_client):
        user = UserFactory()
        api_client.force_authenticate(user=user)
        response = api_client.delete(f"/api/customers/{user.id}/")
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_user_can_update_email(self, api_client):
        password = "testpassword"
        user = UserFactory(password=password)
        api_client.force_authenticate(user=user)
        new_email = "new_email@example.com"
        url = f"/api/customers/{user.id}/"
        response = api_client.patch(url, data={"email": new_email})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["email"] == new_email
        user.refresh_from_db()
        assert user.email == new_email
