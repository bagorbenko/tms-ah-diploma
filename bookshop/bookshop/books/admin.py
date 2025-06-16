from django.contrib import admin
from .models import Author, Category, Book, Genre, Publisher, BookInstance


class BooksAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "isbn", "pages_count", "state", "bind")
    list_filter = ("category", "genres", "author", "state", "bind")
    search_fields = ("title", "isbn", "summary")


class BookInstancesAdmin(admin.ModelAdmin):
    list_display = ("book", "publisher", "price", "count")
    list_filter = ("publisher",)
    search_fields = ("book__title", "publisher__name")


admin.site.register(Category)
admin.site.register(Book, BooksAdmin)
admin.site.register(Genre)
admin.site.register(Author)
admin.site.register(Publisher)
admin.site.register(BookInstance, BookInstancesAdmin)
