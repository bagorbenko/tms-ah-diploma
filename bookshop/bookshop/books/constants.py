from django.db import models
from django.utils.translation import gettext_lazy as _


class States(models.TextChoices):
    NEW = "N", _("Новая")
    USED = "U", _("Б.У.")


class Binding(models.TextChoices):
    SOFTCOVER = "SC", _("Мягкая")
    HARDCOVER = "HC", _("Твердая")
    SPRING = "SP", _("Пружинная")
    BRACKET = "BR", _("Скобой")
    BOLTED = "BL", _("Болтом")
