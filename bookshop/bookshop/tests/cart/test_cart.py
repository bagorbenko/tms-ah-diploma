import pytest
from django.contrib.auth import get_user_model
from rest_framework import status

from tests.factories import BookInstanceFactory
from tests.factories import UserFactory


@pytest.mark.django_db
class TestsCart:
    endpoint = "/api/registration/"
    endpoint_cart = "/api/carts/"

    def test_create_cart(self, api_client, user_data):
        response = api_client.post(self.endpoint, data=user_data, format="json")
        assert response.status_code == status.HTTP_201_CREATED
        user = get_user_model().objects.get(username=user_data["username"])
        assert user.cart

    def test_add_book_to_cart(self, api_client):
        user = UserFactory()
        api_client.force_authenticate(user)
        cart = user.cart
        book = BookInstanceFactory(count=3)
        response = api_client.post(
            f"/api/cart_items/",
            data={"count": book.count, "book_instance": book.id, "cart": cart.id},
            format="json",
        )
        assert response.status_code == status.HTTP_201_CREATED

    def test_add_book_to_cart_with_more_books_than_in_store(self, api_client):
        user = UserFactory()
        api_client.force_authenticate(user)
        cart = user.cart
        book = BookInstanceFactory(count=3)
        response = api_client.post(
            f"/api/cart_items/",
            data={"count": book.count + 1, "book_instance": book.id, "cart": cart.id},
            format="json",
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Недостаточно книг в магазине" in response.data["count"]
