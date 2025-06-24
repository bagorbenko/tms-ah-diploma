import pytest
from app import create_app, db
from app.models.author import Author
from app.models.category import Category
from app.models.book import Book
from app.models.user import User

@pytest.fixture
def app():
    """Создание тестового приложения"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Тестовый клиент"""
    return app.test_client()

@pytest.fixture
def test_user(app):
    """Создание тестового пользователя"""
    with app.app_context():
        # Проверяем, существует ли уже пользователь
        existing_user = User.query.filter_by(username='testuser').first()
        if existing_user:
            return existing_user
            
        user = User(
            username='testuser',
            email='test@example.com',
            first_name='Test',
            last_name='User'
        )
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        # Возвращаем свежий объект из базы
        return User.query.filter_by(username='testuser').first()

@pytest.fixture
def test_author(app):
    """Создание тестового автора"""
    with app.app_context():
        # Проверяем, существует ли уже автор
        existing_author = Author.query.filter_by(name='Test Author').first()
        if existing_author:
            return existing_author
            
        author = Author(
            name='Test Author',
            bio='Test bio'
        )
        db.session.add(author)
        db.session.commit()
        
        # Возвращаем свежий объект из базы
        return Author.query.filter_by(name='Test Author').first()

@pytest.fixture
def test_category(app):
    """Создание тестовой категории"""
    with app.app_context():
        # Проверяем, существует ли уже категория
        existing_category = Category.query.filter_by(name='Test Category').first()
        if existing_category:
            return existing_category
            
        category = Category(
            name='Test Category',
            description='Test description'
        )
        db.session.add(category)
        db.session.commit()
        
        # Возвращаем свежий объект из базы
        return Category.query.filter_by(name='Test Category').first()

@pytest.fixture
def test_book(app, test_author, test_category):
    """Создание тестовой книги"""
    with app.app_context():
        # Получаем свежие объекты из базы
        author = Author.query.get(test_author.id)
        category = Category.query.get(test_category.id)
        
        # Проверяем, существует ли уже книга
        existing_book = Book.query.filter_by(title='Test Book').first()
        if existing_book:
            return existing_book
            
        book = Book(
            title='Test Book',
            isbn='978-1234567890',
            price=1500.00,
            description='Test book description',
            stock_quantity=10,
            author_id=author.id,
            category_id=category.id
        )
        db.session.add(book)
        db.session.commit()
        
        # Возвращаем свежий объект из базы
        return Book.query.filter_by(title='Test Book').first() 