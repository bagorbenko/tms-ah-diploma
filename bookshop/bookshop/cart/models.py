from django.db import models
from rest_framework import exceptions

from user.models import User
from books.models import BookInstance
from django.db.models.signals import post_save
from django.dispatch import receiver


class CartItem(models.Model):
    book_instance = models.ForeignKey(
        BookInstance, on_delete=models.CASCADE, related_name="book_instance"
    )
    cart = models.ForeignKey(
        "Cart", on_delete=models.CASCADE, related_name="cart_items"
    )
    count = models.IntegerField()
    price = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, editable=False
    )

    def get_total_price(self):
        self.price = self.book_instance.price * self.count
        return self.price

    def save(self, *args, **kwargs):
        if self.count > self.book_instance.count:
            raise exceptions.ValidationError({"count": "Недостаточно книг в магазине"})
        self.price = self.book_instance.price * self.count
        super(CartItem, self).save(*args, **kwargs)
        self.cart.update_total_price()

    def __str__(self):
        return f"{self.count} шт. книги {self.book_instance.book.title} по цене {self.price}"


class Cart(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, unique=True, related_name="cart"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    total_price = models.DecimalField(
        decimal_places=2, max_digits=10, default=0, editable=False
    )

    def total_items(self):
        return self.cart_items.count()

    def update_total_price(self):
        total_price = 0
        for item in self.cart_items.all():
            total_price += item.get_total_price()
        self.total_price = total_price
        self.save()

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"

    @receiver(post_save, sender=User)
    def create_cart(sender, instance, created, **kwargs):
        if created:
            Cart.objects.create(user=instance)
