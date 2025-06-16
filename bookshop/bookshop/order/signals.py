# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from .models import Order


# @receiver(post_save, sender=Order)
# def update_book_instance(sender, instance, **kwargs):
#     for item in instance.cart.cart_items.all():
#         book_instance = item.book_instance
#         book_instance.count -= item.count
#         book_instance.save()
#
#
# @receiver(post_save, sender=Order)
# def clear_cart(sender, instance, **kwargs):
#     instance.cart.delete
#
#
# @receiver(post_save, sender=Order)
# def update_cart_total_price(sender, instance, created, **kwargs):
#     if created:
#         cart = instance.cart
#         cart.update_total_price()
