import os
import requests
from django.db import models, transaction

from cart.models import Cart
from user.models import User


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="order")
    total_price = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, editable=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Заказ {self.pk} для пользователя {self.user.first_name}"

    def calculate_total_price(self):
        items = self.cart.cart_items.all()
        total_price = 0
        for item in items:
            total_price += item.count * item.book_instance.price
        return total_price

    def send_purchase_data(self):
        # Пропускаем отправку данных в тестовой среде
        if os.getenv('TESTING') == 'true' or os.getenv('DATABASE_URL', '').startswith('sqlite'):
            print("Тестовая среда: отправка данных в API пропущена")
            return
            
        data = []
        for item in self.cart.cart_items.all():
            authors = ", ".join(
                [author.name for author in item.book_instance.book.author.all()]
            )
            item_data = {
                "order_id": self.id,
                "book_id": item.book_instance.book.id,
                "user_id": self.user.id,
                "book_title": item.book_instance.book.title,
                "author_name": authors,
                "price": int(item.price),
                "create_at": self.created_at.strftime("%Y-%m-%d"),
                "publisher_id": item.book_instance.publisher.id,
            }
            data.append(item_data)
        print("\n\n", data)
        
        try:
            # Используем переменную окружения для URL API
            api_url = os.getenv('API_STORE_URL', 'http://api_store:5050')
            requests.post(f"{api_url}/purchases/", json=data, timeout=5)
        except requests.exceptions.RequestException as e:
            print(f"Ошибка отправки данных в API: {e}")
            # В продакшене можно логировать ошибку или добавить в очередь для повторной отправки

    def check_book_availability(self):
        for item in self.cart.cart_items.all():
            if item.book_instance.count < item.count:
                raise ValueError("Не хватает книг в магазине")

    def remove_book_instances(self):
        for item in self.cart.cart_items.all():
            item.book_instance.count -= item.count
            item.book_instance.save()
            item.delete()

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.check_book_availability()
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)
        self.send_purchase_data()
        self.remove_book_instances()
        self.cart.cart_items.all().delete()
        self.cart.update_total_price()

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
