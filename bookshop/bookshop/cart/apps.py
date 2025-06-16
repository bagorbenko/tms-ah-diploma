from django.apps import AppConfig


default_app_config = "cart.apps.AppConfig"


class CartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "cart"
