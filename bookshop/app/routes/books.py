from flask import Blueprint, request, jsonify
from app import db
from app.models.book import Book
from app.models.author import Author
from app.models.category import Category
from datetime import datetime
books_bp = Blueprint('books', __name__)
@books_bp.route('/books', methods=['GET'])
def get_books():
    """Получить все книги с поиском и фильтрацией"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        search = request.args.get('search', '').strip()
        author_id = request.args.get('author_id', type=int)
        category_id = request.args.get('category_id', type=int)
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        in_stock = request.args.get('in_stock', type=bool)
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc')
        query = Book.query
        if search:
            query = query.filter(
                db.or_(
                    Book.title.ilike(f'%{search}%'),
                    Book.description.ilike(f'%{search}%'),
                    Book.isbn.ilike(f'%{search}%')
                )
            )
        if author_id:
            query = query.filter(Book.author_id == author_id)
        if category_id:
            query = query.filter(Book.category_id == category_id)
        if min_price is not None:
            query = query.filter(Book.price >= min_price)
        if max_price is not None:
            query = query.filter(Book.price <= max_price)
        if in_stock is not None:
            if in_stock:
                query = query.filter(Book.stock_quantity > 0, Book.is_available == True)
            else:
                query = query.filter(db.or_(Book.stock_quantity <= 0, Book.is_available == False))
        if hasattr(Book, sort_by):
            if sort_order.lower() == 'desc':
                query = query.order_by(getattr(Book, sort_by).desc())
            else:
                query = query.order_by(getattr(Book, sort_by).asc())
        pagination = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        return jsonify({
            'books': [book.to_dict(include_relations=True) for book in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            'filters_applied': {
                'search': search,
                'author_id': author_id,
                'category_id': category_id,
                'min_price': min_price,
                'max_price': max_price,
                'in_stock': in_stock,
                'sort_by': sort_by,
                'sort_order': sort_order
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@books_bp.route('/books', methods=['POST'])
def create_book():
    """Создать новую книгу"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных в запросе'}), 400
        required_fields = ['title', 'author_id', 'category_id', 'price']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Поле {field} обязательно'}), 400
        author = Author.query.get(data['author_id'])
        if not author:
            return jsonify({'error': 'Автор не найден'}), 404
        category = Category.query.get(data['category_id'])
        if not category:
            return jsonify({'error': 'Категория не найдена'}), 404
        if data.get('isbn'):
            existing_book = Book.query.filter_by(isbn=data['isbn']).first()
            if existing_book:
                return jsonify({'error': 'Книга с таким ISBN уже существует'}), 400
        book = Book(
            title=data['title'],
            isbn=data.get('isbn'),
            price=data['price'],
            description=data.get('description'),
            pages=data.get('pages'),
            publication_date=datetime.strptime(data['publication_date'], '%Y-%m-%d').date() if data.get('publication_date') else None,
            stock_quantity=data.get('stock_quantity', 0),
            image_url=data.get('image_url'),
            is_available=data.get('is_available', True),
            author_id=data['author_id'],
            category_id=data['category_id']
        )
        db.session.add(book)
        db.session.commit()
        return jsonify({
            'message': 'Книга успешно создана',
            'book': book.to_dict(include_relations=True)
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@books_bp.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Получить книгу по ID"""
    try:
        book = Book.query.get_or_404(book_id)
        return jsonify(book.to_dict(include_relations=True))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@books_bp.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Обновить книгу"""
    try:
        book = Book.query.get_or_404(book_id)
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных в запросе'}), 400
        if 'isbn' in data and data['isbn'] != book.isbn:
            existing_book = Book.query.filter_by(isbn=data['isbn']).first()
            if existing_book:
                return jsonify({'error': 'Книга с таким ISBN уже существует'}), 400
        if 'author_id' in data:
            author = Author.query.get(data['author_id'])
            if not author:
                return jsonify({'error': 'Автор не найден'}), 404
        if 'category_id' in data:
            category = Category.query.get(data['category_id'])
            if not category:
                return jsonify({'error': 'Категория не найдена'}), 404
        updatable_fields = [
            'title', 'isbn', 'price', 'description', 'pages', 
            'stock_quantity', 'image_url', 'is_available', 
            'author_id', 'category_id'
        ]
        for field in updatable_fields:
            if field in data:
                setattr(book, field, data[field])
        if 'publication_date' in data and data['publication_date']:
            book.publication_date = datetime.strptime(data['publication_date'], '%Y-%m-%d').date()
        book.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({
            'message': 'Книга успешно обновлена',
            'book': book.to_dict(include_relations=True)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@books_bp.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Удалить книгу"""
    try:
        book = Book.query.get_or_404(book_id)
        if book.order_items:
            return jsonify({
                'error': 'Нельзя удалить книгу, которая есть в заказах. Деактивируйте её вместо удаления.'
            }), 400
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Книга успешно удалена'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@books_bp.route('/books/search', methods=['GET'])
def search_books():
    """Расширенный поиск книг"""
    try:
        query_text = request.args.get('q', '').strip()
        if not query_text:
            return jsonify({'error': 'Параметр поиска q обязателен'}), 400
        books = Book.query.join(Author).join(Category).filter(
            db.or_(
                Book.title.ilike(f'%{query_text}%'),
                Book.description.ilike(f'%{query_text}%'),
                Book.isbn.ilike(f'%{query_text}%'),
                Author.name.ilike(f'%{query_text}%'),
                Category.name.ilike(f'%{query_text}%')
            )
        ).limit(50).all()
        return jsonify({
            'query': query_text,
            'results_count': len(books),
            'books': [book.to_dict(include_relations=True) for book in books]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 