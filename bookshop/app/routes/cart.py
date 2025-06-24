from flask import Blueprint, request, jsonify
from app import db
from app.models.cart import CartItem
from app.models.book import Book
from app.models.user import User

cart_bp = Blueprint('cart', __name__)

@cart_bp.route('/cart/<int:user_id>', methods=['GET'])
def get_cart(user_id):
    """Получить корзину пользователя"""
    try:
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        total = sum(item.total_price for item in cart_items)
        
        return jsonify({
            'user_id': user_id,
            'items': [item.to_dict() for item in cart_items],
            'items_count': len(cart_items),
            'total_quantity': sum(item.quantity for item in cart_items),
            'total_price': total
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart/add', methods=['POST'])
def add_to_cart():
    """Добавить книгу в корзину"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных в запросе'}), 400
        
        user_id = data.get('user_id')
        book_id = data.get('book_id')
        quantity = data.get('quantity', 1)
        
        if not user_id or not book_id:
            return jsonify({'error': 'user_id и book_id обязательны'}), 400
        
        # Проверяем существование пользователя и книги
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404
        
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'error': 'Книга не найдена'}), 404
        
        if not book.is_in_stock:
            return jsonify({'error': 'Книга недоступна или нет в наличии'}), 400
        
        # Проверяем, есть ли уже эта книга в корзине
        existing_item = CartItem.query.filter_by(user_id=user_id, book_id=book_id).first()
        
        if existing_item:
            # Обновляем количество
            existing_item.quantity += quantity
            db.session.commit()
            cart_item = existing_item
        else:
            # Создаем новый элемент корзины
            cart_item = CartItem(
                user_id=user_id,
                book_id=book_id,
                quantity=quantity
            )
            db.session.add(cart_item)
            db.session.commit()
        
        return jsonify({
            'message': 'Книга добавлена в корзину',
            'cart_item': cart_item.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart/<int:item_id>', methods=['PUT'])
def update_cart_item(item_id):
    """Обновить количество в корзине"""
    try:
        cart_item = CartItem.query.get_or_404(item_id)
        data = request.get_json()
        
        if 'quantity' in data:
            quantity = data['quantity']
            if quantity <= 0:
                # Удаляем элемент если количество 0 или меньше
                db.session.delete(cart_item)
                db.session.commit()
                return jsonify({'message': 'Элемент удален из корзины'})
            else:
                cart_item.quantity = quantity
                db.session.commit()
        
        return jsonify({
            'message': 'Корзина обновлена',
            'cart_item': cart_item.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    """Удалить элемент из корзины"""
    try:
        cart_item = CartItem.query.get_or_404(item_id)
        db.session.delete(cart_item)
        db.session.commit()
        
        return jsonify({'message': 'Элемент удален из корзины'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@cart_bp.route('/cart/clear/<int:user_id>', methods=['DELETE'])
def clear_cart(user_id):
    """Очистить корзину пользователя"""
    try:
        CartItem.query.filter_by(user_id=user_id).delete()
        db.session.commit()
        
        return jsonify({'message': 'Корзина очищена'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 