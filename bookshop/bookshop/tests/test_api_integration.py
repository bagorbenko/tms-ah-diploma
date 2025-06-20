import pytest
from unittest.mock import patch
from tests.factories import UserFactory, CartItemFactory, BookInstanceFactory
from order.models import Order


@pytest.mark.django_db
def test_order_api_call_mocked(mock_api_requests):
    """Тест проверяет что HTTP запрос к API корректно мокируется"""
    user = UserFactory()
    cart = user.cart
    book = BookInstanceFactory(count=5)
    cart_item = CartItemFactory(cart=cart, book_instance=book, count=2)
    
    # Временно отключаем переменные TESTING и DATABASE_URL для проверки мока
    with patch.dict('os.environ', {'TESTING': 'false', 'DATABASE_URL': 'postgresql://test:test@localhost:5432/test'}):
        order = Order(user=user, cart=cart)
        order.save()
        
        # Проверяем что мок был вызван
        assert mock_api_requests.called
        
        # Проверяем параметры вызова
        call_args = mock_api_requests.call_args
        assert call_args is not None
        assert '/purchases/' in call_args[0][0]  # URL содержит /purchases/
        assert 'json' in call_args[1]  # Есть JSON данные


@pytest.mark.django_db  
def test_order_in_testing_mode():
    """Тест проверяет что в тестовом режиме HTTP запросы пропускаются"""
    user = UserFactory()
    cart = user.cart
    book = BookInstanceFactory(count=5)
    cart_item = CartItemFactory(cart=cart, book_instance=book, count=2)
    
    # В тестовом режиме (TESTING=true или SQLite) запросы должны пропускаться
    order = Order(user=user, cart=cart)
    order.save()
    
    # Проверяем что заказ создался успешно без HTTP запроса
    assert Order.objects.filter(id=order.id).exists()
    assert order.total_price > 0


@pytest.mark.django_db
def test_order_with_disabled_api_calls(mock_api_requests):
    """Тест проверяет что при DISABLE_API_CALLS=true запросы пропускаются"""
    user = UserFactory()
    cart = user.cart
    book = BookInstanceFactory(count=5)
    cart_item = CartItemFactory(cart=cart, book_instance=book, count=2)
    
    # Используем DISABLE_API_CALLS для отключения API вызовов
    with patch.dict('os.environ', {'DISABLE_API_CALLS': 'true', 'DATABASE_URL': 'postgresql://test:test@localhost:5432/test'}):
        order = Order(user=user, cart=cart)
        order.save()
        
        # Проверяем что заказ создался успешно
        assert Order.objects.filter(id=order.id).exists()
        assert order.total_price > 0
        
        # Проверяем что мок НЕ был вызван
        assert not mock_api_requests.called 