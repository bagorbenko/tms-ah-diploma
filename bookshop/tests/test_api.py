import json
import pytest
def test_health_check(client):
    """Тест health check endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert data['service'] == 'Bookshop Flask API'
def test_simple_health(client):
    """Тест простого health check"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
def test_api_docs(client):
    """Тест документации API"""
    response = client.get('/api/docs')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['title'] == 'Bookshop API Documentation'
def test_get_books_empty(client):
    """Тест получения пустого списка книг"""
    response = client.get('/api/books')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'books' in data
    assert isinstance(data['books'], list)
def test_get_authors_empty(client):
    """Тест получения пустого списка авторов"""
    response = client.get('/api/authors')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'authors' in data
    assert data['count'] == 0
def test_get_categories_empty(client):
    """Тест получения пустого списка категорий"""
    response = client.get('/api/categories')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'categories' in data
    assert data['count'] == 0
def test_create_author(client):
    """Тест создания автора"""
    author_data = {
        'name': 'Test Author',
        'bio': 'Test biography',
        'nationality': 'Test Country'
    }
    response = client.post('/api/authors', 
                          data=json.dumps(author_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Автор создан'
    assert data['author']['name'] == 'Test Author'
def test_create_category(client):
    """Тест создания категории"""
    category_data = {
        'name': 'Test Category',
        'description': 'Test description'
    }
    response = client.post('/api/categories',
                          data=json.dumps(category_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Категория создана'
    assert data['category']['name'] == 'Test Category'
def test_create_book(client, test_author, test_category):
    """Тест создания книги"""
    book_data = {
        'title': 'Test Book',
        'isbn': '978-1234567890',
        'price': 1500.00,
        'description': 'Test book description',
        'pages': 300,
        'stock_quantity': 10,
        'author_id': test_author.id,
        'category_id': test_category.id
    }
    response = client.post('/api/books',
                          data=json.dumps(book_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Книга успешно создана'
    assert data['book']['title'] == 'Test Book'
def test_add_to_cart(client, test_user, test_book):
    """Тест добавления книги в корзину"""
    cart_data = {
        'user_id': test_user.id,
        'book_id': test_book.id,
        'quantity': 2
    }
    response = client.post('/api/cart/add',
                          data=json.dumps(cart_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Книга добавлена в корзину'
def test_get_cart(client, test_user):
    """Тест получения корзины"""
    response = client.get(f'/api/cart/{test_user.id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['user_id'] == test_user.id
    assert 'items' in data
    assert 'total_price' in data
def test_create_user(client):
    """Тест создания пользователя"""
    user_data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'first_name': 'New',
        'last_name': 'User',
        'password': 'password123'
    }
    response = client.post('/api/users',
                          data=json.dumps(user_data),
                          content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['message'] == 'Пользователь создан'
    assert data['user']['username'] == 'newuser' 