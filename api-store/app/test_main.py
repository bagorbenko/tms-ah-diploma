import factory
import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import PurchaseModel
from app.database import Base
from app.main import app, get_db
import os

fake = Faker()

# Создаем отдельную тестовую базу данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///:memory:")
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    """Настройка тестовой базы данных"""
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    # Импортируем приложение из пакета app
    return TestClient(app)


class PurchaseFactory(factory.Factory):
    class Meta:
        model = PurchaseModel

    order_id = factory.LazyAttribute(lambda o: fake.random_int(min=1, max=500, step=1))
    book_id = factory.LazyAttribute(lambda o: fake.random_int(min=1, max=1000, step=1))
    user_id = factory.LazyAttribute(lambda o: fake.random_int(min=1, max=20, step=1))
    book_title = factory.LazyAttribute(lambda o: fake.word())
    author_name = factory.LazyAttribute(lambda o: fake.name())
    price = factory.LazyAttribute(lambda o: fake.random_int(min=100, max=5000, step=1))
    create_at = factory.LazyAttribute(lambda o: str(fake.date()))
    publisher_id = factory.LazyAttribute(lambda o: fake.random_int(min=1, max=20, step=1))

    @classmethod
    def as_dict(cls, **kwargs):
        purchase = cls.create(**kwargs)
        return {
            "order_id": purchase.order_id,
            "book_id": purchase.book_id,
            "user_id": purchase.user_id,
            "book_title": purchase.book_title,
            "author_name": purchase.author_name,
            "price": purchase.price,
            "create_at": purchase.create_at,
            "publisher_id": purchase.publisher_id,
        }


def test_create_purchase(client):
    # Формируем данные и отправляем POST на /purchases/
    purchase_data = PurchaseFactory.as_dict()
    response = client.post("/purchases/", json=[purchase_data])
    assert response.status_code == 200
