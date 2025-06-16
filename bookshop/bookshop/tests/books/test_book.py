import pytest
from books.models import Book, BookInstance
from tests.factories import (
    CategoryFactory,
    GenreFactory,
    AuthorFactory,
    PublisherFactory,
    BookFactory,
    BookInstanceFactory,
)


@pytest.mark.django_db
def test_category_list_view(api_client):
    category = CategoryFactory()
    response = api_client.get(f"/api/categories/{category.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_genre_list_view(api_client):
    genre = GenreFactory()
    response = api_client.get(f"/api/genres/{genre.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_author_list_view(api_client):
    author = AuthorFactory()
    response = api_client.get(f"/api/authors/{author.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_publisher_list_view(api_client):
    publisher = PublisherFactory()
    response = api_client.get(f"/api/publishers/{publisher.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_book_list_view(api_client):
    book = BookFactory()
    assert isinstance(book, Book)
    response = api_client.get(f"/api/books/{book.id}/")
    assert response.status_code == 200


@pytest.mark.django_db
def test_book_instance_list_view(api_client):
    book_instance = BookInstanceFactory()
    assert isinstance(book_instance, BookInstance)
