from django.db import models
from .constants import States, Binding


class Category(models.Model):
    name = models.CharField(verbose_name="Категория", max_length=150)
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Genre(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=100)
    description = models.TextField(verbose_name="Описание", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Author(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=100)
    biography = models.TextField(verbose_name="Описание", blank=True)
    image = models.ImageField(
        verbose_name="Изображение", upload_to="media/authors/", blank=True
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"


class Publisher(models.Model):
    name = models.CharField(verbose_name="Имя", max_length=100)
    description = models.TextField(verbose_name="Описание")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Издательство"
        verbose_name_plural = "Издательства"


class Book(models.Model):
    title = models.CharField(verbose_name="Название", max_length=100)
    category = models.ForeignKey(
        Category,
        verbose_name="Категория",
        on_delete=models.SET_NULL,
        null=True,
        related_name="books",
    )
    genres = models.ManyToManyField(Genre, verbose_name="жанры", related_name="books")
    author = models.ManyToManyField(Author, verbose_name="автор", related_name="books")
    isbn = models.PositiveIntegerField(verbose_name="isbn", max_length=13, unique=True)
    summary = models.TextField(verbose_name="Описание", max_length=1000, blank=True)
    pages_count = models.PositiveIntegerField()
    state = models.CharField(choices=States.choices, max_length=2, default=States.NEW)
    bind = models.CharField(
        choices=Binding.choices, max_length=2, default=Binding.SOFTCOVER
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = "Книги"


class BookInstance(models.Model):
    book = models.ForeignKey(
        Book,
        verbose_name="Книга",
        on_delete=models.CASCADE,
        null=True,
        related_name="book_instances",
    )
    publisher = models.ForeignKey(
        Publisher, verbose_name="Издательство", on_delete=models.SET_NULL, null=True
    )
    price = models.FloatField(verbose_name="Цена", max_length=10)
    count = models.PositiveIntegerField(verbose_name="Количество")

    def __str__(self):
        return f"{self.book.title} - {self.publisher.name}"

    class Meta:
        verbose_name = "Книга Издателя"
        verbose_name_plural = "Книги Издателя"
