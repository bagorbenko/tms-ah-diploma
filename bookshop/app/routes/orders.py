from flask import Blueprint, request, jsonify, current_app
from app import db
from app.models.order import Order, OrderItem, OrderStatus
from app.models.cart import CartItem
from app.models.user import User
from app.services.api_store_service import ApiStoreService
import uuid
from datetime import datetime

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/orders', methods=['GET'])
def get_orders():
    """Получить все заказы"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        status = request.args.get('status')
        user_id = request.args.get('user_id', type=int)
        
        query = Order.query
        
        if status:
            query = query.filter(Order.status == OrderStatus(status))
        if user_id:
            query = query.filter(Order.user_id == user_id)
        
        query = query.order_by(Order.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'orders': [order.to_dict() for order in pagination.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': pagination.total,
                'pages': pagination.pages
            }
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders', methods=['POST'])
def create_order():
    """Создать заказ из корзины"""
    try:
        data = request.get_json()
        if not data or 'user_id' not in data:
            return jsonify({'error': 'user_id обязателен'}), 400
        
        user_id = data['user_id']
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Пользователь не найден'}), 404
        
        # Получаем элементы корзины
        cart_items = CartItem.query.filter_by(user_id=user_id).all()
        if not cart_items:
            return jsonify({'error': 'Корзина пуста'}), 400
        
        # Создаем заказ
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        total_amount = sum(item.total_price for item in cart_items)
        
        order = Order(
            order_number=order_number,
            user_id=user_id,
            total_amount=total_amount,
            shipping_address=data.get('shipping_address', user.address),
            notes=data.get('notes')
        )
        
        db.session.add(order)
        db.session.flush()  # Получаем ID заказа
        
        # Создаем элементы заказа
        for cart_item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                book_id=cart_item.book_id,
                quantity=cart_item.quantity,
                price_at_time=cart_item.book.price
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        # Отправляем в API Store
        api_store_service = ApiStoreService()
        api_store_result = api_store_service.send_order(order)
        
        # Обновляем статус заказа
        order.api_store_status = api_store_result['status']
        if 'response' in api_store_result:
            order.api_store_response = api_store_result['response']
        
        # Очищаем корзину после успешного создания заказа
        CartItem.query.filter_by(user_id=user_id).delete()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Заказ успешно создан',
            'order': order.to_dict(include_items=True),
            'api_store_integration': api_store_result
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Получить заказ по ID"""
    try:
        order = Order.query.get_or_404(order_id)
        return jsonify(order.to_dict(include_items=True))
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    """Обновить статус заказа"""
    try:
        order = Order.query.get_or_404(order_id)
        data = request.get_json()
        
        if 'status' in data:
            try:
                order.status = OrderStatus(data['status'])
            except ValueError:
                return jsonify({'error': 'Неверный статус заказа'}), 400
        
        if 'notes' in data:
            order.notes = data['notes']
        
        if 'shipping_address' in data:
            order.shipping_address = data['shipping_address']
        
        order.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Заказ обновлен',
            'order': order.to_dict(include_items=True)
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@orders_bp.route('/orders/user/<int:user_id>', methods=['GET'])
def get_user_orders(user_id):
    """Получить заказы пользователя"""
    try:
        user = User.query.get_or_404(user_id)
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
        
        return jsonify({
            'user_id': user_id,
            'user': user.to_dict(),
            'orders_count': len(orders),
            'orders': [order.to_dict() for order in orders]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500 