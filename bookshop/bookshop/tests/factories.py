import factory
from faker import Faker
from books.models import Category, Genre, Author, Publisher, Book, BookInstance


from order.models import Order
from user.models import User
from cart.models import Cart, CartItem
from books.models import BookInstance


fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Faker("user_name")
    email = factory.Faker("email")


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Genre

    name = factory.LazyAttribute(lambda o: fake.word())
    description = factory.LazyAttribute(lambda o: fake.text())


class AuthorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Author

    name = factory.LazyAttribute(lambda o: fake.name())
    biography = factory.LazyAttribute(lambda o: fake.text())


class PublisherFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Publisher

    name = factory.LazyAttribute(lambda o: fake.company_suffix())
    description = factory.LazyAttribute(lambda o: fake.text())


class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    title = factory.LazyAttribute(lambda o: fake.word())
    isbn = factory.LazyAttribute(lambda o: fake.pyint())
    summary = factory.LazyAttribute(lambda o: fake.text())
    pages_count = factory.LazyAttribute(
        lambda o: fake.random_int(min=100, max=500, step=1)
    )

    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for genre in extracted:
                self.genres.add(genre)

    @factory.post_generation
    def author(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for author in extracted:
                self.author.add(author)

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for category in extracted:
                self.category.add(category)


class BookInstanceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = BookInstance

    book = factory.SubFactory(BookFactory)
    publisher = factory.SubFactory(PublisherFactory)
    price = factory.LazyAttribute(lambda o: fake.random_int(min=100, max=5000, step=1))
    count = factory.LazyAttribute(lambda o: fake.random_int(min=1, max=100, step=1))


class CartFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory)


class CartItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CartItem

    cart = factory.SubFactory(CartFactory)
    book_instance = factory.SubFactory(BookInstanceFactory)
    count = factory.Faker("random_int", min=1, max=5)


class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda o: fake.word())
    description = factory.LazyAttribute(lambda o: fake.text())
