from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import json
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Данные для демонстрации
books = [
    {'id': 1, 'title': 'Чистый код', 'author': 'Роберт Мартин', 'price': 1500, 'isbn': '978-5-4461-0923-4', 'category': 'Программирование'},
    {'id': 2, 'title': 'Архитектура ПО', 'author': 'Мартин Фаулер', 'price': 2000, 'isbn': '978-5-4461-0924-1', 'category': 'Архитектура'},
    {'id': 3, 'title': 'Python для профессионалов', 'author': 'Дэн Бейдер', 'price': 1800, 'isbn': '978-5-4461-0925-8', 'category': 'Python'},
    {'id': 4, 'title': 'Проектирование API', 'author': 'Арно Лорет', 'price': 2200, 'isbn': '978-5-4461-0926-5', 'category': 'API'},
    {'id': 5, 'title': 'Kubernetes в действии', 'author': 'Марко Лукша', 'price': 2500, 'isbn': '978-5-4461-0927-2', 'category': 'DevOps'}
]

authors = [
    {'id': 1, 'name': 'Роберт Мартин', 'bio': 'Известный автор книг по программированию'},
    {'id': 2, 'name': 'Мартин Фаулер', 'bio': 'Эксперт по архитектуре ПО'},
    {'id': 3, 'name': 'Дэн Бейдер', 'bio': 'Python разработчик и тренер'},
    {'id': 4, 'name': 'Арно Лорет', 'bio': 'Архитектор API'},
    {'id': 5, 'name': 'Марко Лукша', 'bio': 'Kubernetes эксперт'}
]

categories = [
    {'id': 1, 'name': 'Программирование'},
    {'id': 2, 'name': 'Архитектура'},
    {'id': 3, 'name': 'Python'},
    {'id': 4, 'name': 'API'},
    {'id': 5, 'name': 'DevOps'}
]

cart = []
orders = []
users = [
    {'id': 1, 'username': 'admin', 'email': 'admin@bookshop.com', 'first_name': 'Admin', 'last_name': 'User'}
]

# URL API Store для интеграции
API_STORE_URL = os.getenv('API_STORE_URL', 'http://api-store-service.api-store-prod.svc.cluster.local')

@app.route('/')
def health_check():
    return jsonify({
        'service': 'Bookshop Flask',
        'status': 'healthy',
        'version': '1.0.0',
        'books_count': len(books),
        'orders_count': len(orders),
        'cart_items': len(cart),
        'api_store_url': API_STORE_URL,
        'endpoints': {
            'GET /': 'Health check',
            'GET /api/books': 'Получить все книги',
            'GET /api/books/<id>': 'Получить книгу по ID',
            'GET /api/authors': 'Получить всех авторов',
            'GET /api/categories': 'Получить все категории',
            'POST /api/cart/add': 'Добавить книгу в корзину',
            'GET /api/cart': 'Посмотреть корзину',
            'DELETE /api/cart': 'Очистить корзину',
            'POST /api/orders': 'Создать заказ',
            'GET /api/orders': 'Получить заказы',
            'GET /api/users': 'Получить пользователей'
        }
    })

# Books API
@app.route('/api/books', methods=['GET'])
def get_books():
    return jsonify({
        'count': len(books),
        'results': books
    })

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b['id'] == book_id), None)
    if not book:
        return jsonify({'error': 'Книга не найдена'}), 404
    return jsonify(book)

# Authors API
@app.route('/api/authors', methods=['GET'])
def get_authors():
    return jsonify({
        'count': len(authors),
        'results': authors
    })

# Categories API
@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify({
        'count': len(categories),
        'results': categories
    })

# Cart API
@app.route('/api/cart', methods=['GET'])
def get_cart():
    total = sum(item['price'] * item['quantity'] for item in cart)
    return jsonify({
        'items': cart,
        'total': total,
        'count': len(cart),
        'item_count': sum(item['quantity'] for item in cart)
    })

@app.route('/api/cart/add', methods=['POST'])
def add_to_cart():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных в запросе'}), 400
            
        book_id = data.get('book_id')
        quantity = data.get('quantity', 1)
        
        if not book_id:
            return jsonify({'error': 'book_id обязателен'}), 400
        
        book = next((b for b in books if b['id'] == book_id), None)
        if not book:
            return jsonify({'error': 'Книга не найдена'}), 404
        
        # Проверяем есть ли уже эта книга в корзине
        existing_item = next((item for item in cart if item['book_id'] == book_id), None)
        if existing_item:
            existing_item['quantity'] += quantity
            cart_item = existing_item
        else:
            cart_item = {
                'book_id': book_id,
                'title': book['title'],
                'author': book['author'],
                'price': book['price'],
                'quantity': quantity
            }
            cart.append(cart_item)
        
        return jsonify({
            'message': 'Книга добавлена в корзину',
            'item': cart_item,
            'cart_total': sum(item['price'] * item['quantity'] for item in cart)
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/cart', methods=['DELETE'])
def clear_cart():
    cart.clear()
    return jsonify({'message': 'Корзина очищена'}), 200

# Orders API
@app.route('/api/orders', methods=['GET'])
def get_orders():
    return jsonify({
        'count': len(orders),
        'results': orders
    })

@app.route('/api/orders', methods=['POST'])
def create_order():
    try:
        if not cart:
            return jsonify({'error': 'Корзина пуста'}), 400
        
        order_id = len(orders) + 1
        order = {
            'id': order_id,
            'items': cart.copy(),
            'total': sum(item['price'] * item['quantity'] for item in cart),
            'created_at': datetime.now().isoformat(),
            'status': 'created',
            'user_id': 1  # По умолчанию admin user
        }
        orders.append(order)
        
        # Подготавливаем данные для отправки в API Store
        purchase_data = []
        for item in cart:
            purchase_data.append({
                'order_id': order_id,
                'book_id': item['book_id'],
                'user_id': 1,
                'book_title': item['title'],
                'author_name': item['author'],
                'price': item['price'] * item['quantity'],
                'create_at': datetime.now().strftime('%Y-%m-%d'),
                'publisher_id': 1
            })
        
        # Отправляем заказ в API Store
        try:
            print(f'📦 Отправка заказа {order_id} в API Store: {API_STORE_URL}')
            response = requests.post(f'{API_STORE_URL}/purchases/', json=purchase_data, timeout=10)
            if response.status_code == 200:
                print(f'✅ Заказ успешно отправлен в API Store')
                order['api_store_status'] = 'sent'
                order['api_store_response'] = response.json()
            else:
                print(f'⚠️ Ошибка отправки в API Store: {response.status_code}')
                order['api_store_status'] = 'failed'
                order['api_store_error'] = f'HTTP {response.status_code}'
        except Exception as e:
            print(f'❌ Ошибка соединения с API Store: {e}')
            order['api_store_status'] = 'connection_error'
            order['api_store_error'] = str(e)
        
        # Очищаем корзину после создания заказа
        cart.clear()
        print(f'🎉 Заказ {order_id} создан! Сумма: {order["total"]} руб.')
        return jsonify(order), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Users API
@app.route('/api/users', methods=['GET'])
def get_users():
    return jsonify({
        'count': len(users),
        'results': users
    })

# Health check endpoint
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

# API Documentation
@app.route('/api/docs')
def api_docs():
    return jsonify({
        'title': 'Bookshop API',
        'version': '1.0.0',
        'description': 'Flask API для управления книжным магазином',
        'endpoints': {
            'books': '/api/books - управление книгами',
            'authors': '/api/authors - управление авторами',
            'categories': '/api/categories - управление категориями',
            'cart': '/api/cart - управление корзиной',
            'orders': '/api/orders - управление заказами',
            'users': '/api/users - управление пользователями'
        }
    })

if __name__ == '__main__':
    print('🚀 Flask Bookshop запущен на порту 8000')
    print(f'🔗 API Store URL: {API_STORE_URL}')
    app.run(host='0.0.0.0', port=8000, debug=True) 