import pytest
from rest_framework import status
import requests

from cart.models import CartItem
from order.models import Order
from tests.factories import BookInstanceFactory
from tests.factories import UserFactory, CartItemFactory, OrderFactory


@pytest.mark.django_db
def test_cart_items_delete_after_order_creation(api_client):
    user = UserFactory()
    api_client.force_authenticate(user)
    cart = user.cart
    book = BookInstanceFactory(count=3)
    cart_item = CartItemFactory(cart=cart, book_instance=book, count=2)
    book.count = 5
    book.save()
    assert CartItem.objects.count() == 1
    url = f"/api/orders/"
    data = {"user": user.id, "cart": cart.id}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert CartItem.objects.count() == 0
    assert Order.objects.count() == 1
    assert Order.objects.filter(user=user, cart=cart).exists()


@pytest.mark.django_db
def test_user_can_see_their_own_orders(api_client):
    user = UserFactory()
    cart = user.cart
    order = OrderFactory(cart=cart, user=user)
    api_client.force_authenticate(user=user)
    response = api_client.get("/api/orders/")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert "created_at" in response.data[0]
    assert response.data[0]["user"] == user.id
    assert response.data[0]["cart"] == cart.id
