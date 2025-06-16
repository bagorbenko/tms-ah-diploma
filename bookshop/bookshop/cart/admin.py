from django.contrib import admin
from .models import Cart, CartItem


class CartItemInline(admin.TabularInline):
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemInline]
    list_display = (
        "user",
        "created_at",
        "updated_at",
        "total_price",
        "total_book_count",
    )
    list_filter = ("created_at",)
    search_fields = ("user__first_name", "user__last_name")
    ordering = ("-created_at",)

    def total_book_count(self, obj):
        count = 0
        for item in obj.cart_items.all():
            count += item.count
        return count

    total_book_count.short_description = "Total Book Count"
