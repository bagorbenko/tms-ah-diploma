from flask import Blueprint, jsonify, current_app, send_from_directory
from app.models.book import Book
from app.models.author import Author
from app.models.category import Category
from app.models.user import User
from app.models.order import Order
from app.models.cart import CartItem
import os
import requests

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Proxy bookshop frontend from Cloud Storage"""
    try:
        # Получаем HTML из Cloud Storage
        response = requests.get('https://storage.googleapis.com/diploma-static-prod-645ba250/bookshop-frontend.html', timeout=10)
        if response.status_code == 200:
            return response.text, 200, {'Content-Type': 'text/html; charset=utf-8'}
        else:
            # Fallback на локальный файл
            app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
            return send_from_directory(app_dir, 'bookshop-frontend.html')
    except Exception as e:
        # Fallback на информационную страницу
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Bookshop - Frontend Loading</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>Bookshop Service</h1>
            <p>Frontend is temporarily unavailable. Please use direct links:</p>
            <ul>
                <li><a href="https://storage.googleapis.com/diploma-static-prod-645ba250/bookshop-frontend.html">Bookshop Frontend</a></li>
                <li><a href="https://storage.googleapis.com/diploma-static-prod-645ba250/api-store-frontend.html">API Store Frontend</a></li>
                <li><a href="/api">API Documentation</a></li>
            </ul>
            <p>Error: {str(e)}</p>
        </body>
        </html>
        """, 200, {'Content-Type': 'text/html; charset=utf-8'}

@main_bp.route('/web')
def web_index():
    """Serve bookshop frontend as main page"""
    # Прямой путь к HTML файлу в корне проекта
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    return send_from_directory(app_dir, 'bookshop-frontend.html')

@main_bp.route('/api')
@main_bp.route('/api/')
@main_bp.route('/status')
def health_check():
    """Health check endpoint с информацией о сервисе"""
    try:
        # Подсчитываем статистику
        books_count = Book.query.count()
        authors_count = Author.query.count()
        categories_count = Category.query.count()
        users_count = User.query.count()
        orders_count = Order.query.count()
        cart_items_count = CartItem.query.count()
        
        return jsonify({
            'service': 'Bookshop Flask API',
            'status': 'healthy',
            'version': '2.0.0',
            'database': 'connected',
            'statistics': {
                'books': books_count,
                'authors': authors_count,
                'categories': categories_count,
                'users': users_count,
                'orders': orders_count,
                'cart_items': cart_items_count
            },
            'api_store_url': current_app.config.get('API_STORE_URL'),
            'endpoints': {
                'GET /': 'Health check и информация о сервисе',
                'GET /health': 'Простой health check',
                'GET /api/docs': 'Документация API',
                'Books API': {
                    'GET /api/books': 'Получить все книги',
                    'POST /api/books': 'Создать книгу',
                    'GET /api/books/<id>': 'Получить книгу по ID',
                    'PUT /api/books/<id>': 'Обновить книгу',
                    'DELETE /api/books/<id>': 'Удалить книгу'
                },
                'Authors API': {
                    'GET /api/authors': 'Получить всех авторов',
                    'POST /api/authors': 'Создать автора',
                    'GET /api/authors/<id>': 'Получить автора по ID',
                    'PUT /api/authors/<id>': 'Обновить автора',
                    'DELETE /api/authors/<id>': 'Удалить автора'
                },
                'Categories API': {
                    'GET /api/categories': 'Получить все категории',
                    'POST /api/categories': 'Создать категорию',
                    'GET /api/categories/<id>': 'Получить категорию по ID',
                    'PUT /api/categories/<id>': 'Обновить категорию',
                    'DELETE /api/categories/<id>': 'Удалить категорию'
                },
                'Cart API': {
                    'GET /api/cart/<user_id>': 'Получить корзину пользователя',
                    'POST /api/cart/add': 'Добавить книгу в корзину',
                    'PUT /api/cart/<item_id>': 'Обновить количество в корзине',
                    'DELETE /api/cart/<item_id>': 'Удалить из корзины',
                    'DELETE /api/cart/clear/<user_id>': 'Очистить корзину'
                },
                'Orders API': {
                    'GET /api/orders': 'Получить все заказы',
                    'POST /api/orders': 'Создать заказ',
                    'GET /api/orders/<id>': 'Получить заказ по ID',
                    'PUT /api/orders/<id>': 'Обновить статус заказа',
                    'GET /api/orders/user/<user_id>': 'Получить заказы пользователя'
                },
                'Users API': {
                    'GET /api/users': 'Получить всех пользователей',
                    'POST /api/users': 'Создать пользователя',
                    'GET /api/users/<id>': 'Получить пользователя по ID',
                    'PUT /api/users/<id>': 'Обновить пользователя',
                    'DELETE /api/users/<id>': 'Удалить пользователя'
                }
            }
        })
    except Exception as e:
        return jsonify({
            'service': 'Bookshop Flask API',
            'status': 'error',
            'error': str(e),
            'database': 'disconnected'
        }), 500

@main_bp.route('/health')
def simple_health():
    """Простой health check для Kubernetes"""
    return jsonify({'status': 'healthy'})

@main_bp.route('/bookshop')
def serve_bookshop_html():
    """Serve bookshop HTML frontend"""
    # Используем тот же путь что и в главном маршруте
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    return send_from_directory(app_dir, 'bookshop-frontend.html')

@main_bp.route('/api/docs')
def api_docs():
    """Документация API"""
    return jsonify({
        'title': 'Bookshop API Documentation',
        'version': '2.0.0',
        'description': 'Полнофункциональный REST API для управления книжным магазином',
        'base_url': '/api',
        'authentication': 'В данной версии аутентификация упрощена (используется user_id)',
        'response_format': 'JSON',
        'error_handling': 'Стандартные HTTP коды ответов',
        'features': [
            'CRUD операции для всех сущностей',
            'Управление корзиной покупок',
            'Система заказов с интеграцией в API Store',
            'Поиск и фильтрация книг',
            'Управление пользователями',
            'Статистика и отчеты'
        ],
        'models': {
            'Book': 'Книги с полной информацией (автор, категория, цена, остаток)',
            'Author': 'Авторы книг с биографией',
            'Category': 'Категории книг',
            'User': 'Пользователи системы',
            'CartItem': 'Элементы корзины покупок',
            'Order': 'Заказы с элементами и статусами',
            'OrderItem': 'Элементы заказов'
        }
    })

@main_bp.route('/frontend')
def frontend():
    """Redirect to main page"""
    # Путь к директории приложения
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    return send_from_directory(app_dir, 'bookshop-frontend.html')

@main_bp.route('/api-store-frontend')
def api_store_frontend():
    """Serve API Store frontend"""
    # Путь к директории приложения
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    return send_from_directory(app_dir, 'api-store-frontend.html')

@main_bp.route('/html')
def html_frontend():
    """Serve HTML frontend (alternative route)"""
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    return send_from_directory(app_dir, 'bookshop-frontend.html')

@main_bp.route('/ui')
def ui_frontend():
    """Serve HTML frontend (UI route)"""
    app_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
    return send_from_directory(app_dir, 'bookshop-frontend.html') 