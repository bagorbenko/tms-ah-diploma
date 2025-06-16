from books.models import Author, Book, BookInstance, Category, Genre, Publisher
from books.serializers import (
    AuthorSerializer,
    BookInstanceSerializer,
    BookSerializer,
    CategorySerializer,
    GenreSerializer,
    PublisherSerializer,
)
from rest_framework import mixins, viewsets


class BookAPIView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookInstanceAPIView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = BookInstance.objects.all()
    serializer_class = BookInstanceSerializer


class AuthorAPIView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


class GenreAPIView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class PublisherAPIView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer


class CategoryAPIView(
    mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet
):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
