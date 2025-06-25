from app import db
from app.models.author import Author
from app.models.category import Category
from app.models.book import Book
from app.models.user import User
from datetime import date, datetime
def seed_initial_data():
    """Заполнение базы данных начальными данными"""
    try:
        if Author.query.count() > 0:
            return  
        print("🌱 Заполнение базы данных начальными данными...")
        categories_data = [
            {'name': 'Программирование', 'description': 'Книги по программированию и разработке ПО'},
            {'name': 'Архитектура ПО', 'description': 'Книги по архитектуре программного обеспечения'},
            {'name': 'Python', 'description': 'Книги по языку программирования Python'},
            {'name': 'DevOps', 'description': 'Книги по DevOps практикам и инструментам'},
            {'name': 'Базы данных', 'description': 'Книги по проектированию и работе с базами данных'},
            {'name': 'Веб-разработка', 'description': 'Книги по веб-разработке и фронтенду'},
            {'name': 'Машинное обучение', 'description': 'Книги по машинному обучению и ИИ'}
        ]
        categories = []
        for cat_data in categories_data:
            category = Category(**cat_data)
            db.session.add(category)
            categories.append(category)
        db.session.flush()  
        authors_data = [
            {'name': 'Роберт Мартин', 'bio': 'Известный автор книг по программированию и чистому коду', 'nationality': 'США'},
            {'name': 'Мартин Фаулер', 'bio': 'Эксперт по архитектуре ПО и рефакторингу', 'nationality': 'Великобритания'},
            {'name': 'Дэн Бейдер', 'bio': 'Python разработчик и тренер', 'nationality': 'Германия'},
            {'name': 'Марко Лукша', 'bio': 'Kubernetes эксперт и автор', 'nationality': 'Словения'},
            {'name': 'Алекс Петров', 'bio': 'Эксперт по базам данных', 'nationality': 'Болгария'},
            {'name': 'Кайл Симпсон', 'bio': 'JavaScript эксперт и автор серии You Dont Know JS', 'nationality': 'США'},
            {'name': 'Андрей Карпатый', 'bio': 'Исследователь в области машинного обучения', 'nationality': 'Чехия'}
        ]
        authors = []
        for auth_data in authors_data:
            author = Author(**auth_data)
            db.session.add(author)
            authors.append(author)
        db.session.flush()  
        books_data = [
            {
                'title': 'Чистый код',
                'isbn': '978-5-4461-0923-4',
                'price': 1500.00,
                'description': 'Руководство по написанию чистого и поддерживаемого кода',
                'pages': 464,
                'publication_date': date(2008, 8, 1),
                'stock_quantity': 25,
                'author_id': authors[0].id,
                'category_id': categories[0].id
            },
            {
                'title': 'Архитектура ПО',
                'isbn': '978-5-4461-0924-1',
                'price': 2000.00,
                'description': 'Принципы проектирования архитектуры программного обеспечения',
                'pages': 352,
                'publication_date': date(2017, 9, 12),
                'stock_quantity': 15,
                'author_id': authors[1].id,
                'category_id': categories[1].id
            },
            {
                'title': 'Python для профессионалов',
                'isbn': '978-5-4461-0925-8',
                'price': 1800.00,
                'description': 'Продвинутые техники программирования на Python',
                'pages': 280,
                'publication_date': date(2019, 3, 15),
                'stock_quantity': 30,
                'author_id': authors[2].id,
                'category_id': categories[2].id
            },
            {
                'title': 'Kubernetes в действии',
                'isbn': '978-5-4461-0927-2',
                'price': 2500.00,
                'description': 'Практическое руководство по Kubernetes',
                'pages': 624,
                'publication_date': date(2020, 11, 10),
                'stock_quantity': 20,
                'author_id': authors[3].id,
                'category_id': categories[3].id
            },
            {
                'title': 'Проектирование баз данных',
                'isbn': '978-5-4461-0928-9',
                'price': 2200.00,
                'description': 'Основы проектирования эффективных баз данных',
                'pages': 456,
                'publication_date': date(2021, 5, 20),
                'stock_quantity': 18,
                'author_id': authors[4].id,
                'category_id': categories[4].id
            },
            {
                'title': 'Современный JavaScript',
                'isbn': '978-5-4461-0929-6',
                'price': 1900.00,
                'description': 'ES6+ и современные практики JavaScript разработки',
                'pages': 380,
                'publication_date': date(2022, 1, 8),
                'stock_quantity': 22,
                'author_id': authors[5].id,
                'category_id': categories[5].id
            },
            {
                'title': 'Машинное обучение на практике',
                'isbn': '978-5-4461-0930-2',
                'price': 2800.00,
                'description': 'Практическое введение в машинное обучение',
                'pages': 512,
                'publication_date': date(2023, 6, 12),
                'stock_quantity': 12,
                'author_id': authors[6].id,
                'category_id': categories[6].id
            }
        ]
        for book_data in books_data:
            book = Book(**book_data)
            db.session.add(book)
        admin_user = User(
            username='admin',
            email='admin@bookshop.com',
            first_name='Admin',
            last_name='User',
            address='г. Минск, ул. Тестовая, д. 1',
            phone='+375291234567',
            is_admin=True
        )
        admin_user.set_password('admin123')
        db.session.add(admin_user)
        test_user = User(
            username='testuser',
            email='test@bookshop.com',
            first_name='Тест',
            last_name='Пользователь',
            address='г. Минск, ул. Примерная, д. 5',
            phone='+375297654321'
        )
        test_user.set_password('test123')
        db.session.add(test_user)
        db.session.commit()
        print("✅ Начальные данные успешно загружены!")
    except Exception as e:
        db.session.rollback()
        print(f"❌ Ошибка при загрузке начальных данных: {e}")
        raise 