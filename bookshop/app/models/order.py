from app import db
from datetime import datetime
from enum import Enum
class OrderStatus(Enum):
    """Статусы заказа"""
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    PROCESSING = 'processing'
    SHIPPED = 'shipped'
    DELIVERED = 'delivered'
    CANCELLED = 'cancelled'
class Order(db.Model):
    """Модель заказа"""
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    status = db.Column(db.Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    shipping_address = db.Column(db.Text)
    notes = db.Column(db.Text)
    api_store_status = db.Column(db.String(50))  
    api_store_response = db.Column(db.JSON)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    def __repr__(self):
        return f'<Order {self.order_number}>'
    @property
    def items_count(self):
        """Количество элементов в заказе"""
        return sum(item.quantity for item in self.items)
    @property
    def status_display(self):
        """Отображаемое название статуса"""
        status_names = {
            OrderStatus.PENDING: 'Ожидает подтверждения',
            OrderStatus.CONFIRMED: 'Подтвержден',
            OrderStatus.PROCESSING: 'В обработке',
            OrderStatus.SHIPPED: 'Отправлен',
            OrderStatus.DELIVERED: 'Доставлен',
            OrderStatus.CANCELLED: 'Отменен'
        }
        return status_names.get(self.status, str(self.status))
    def to_dict(self, include_items=False):
        """Преобразование в словарь для JSON API"""
        data = {
            'id': self.id,
            'order_number': self.order_number,
            'status': self.status.value if self.status else None,
            'status_display': self.status_display,
            'total_amount': float(self.total_amount) if self.total_amount else 0,
            'shipping_address': self.shipping_address,
            'notes': self.notes,
            'items_count': self.items_count,
            'api_store_status': self.api_store_status,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        if include_items:
            data['items'] = [item.to_dict() for item in self.items]
        return data
class OrderItem(db.Model):
    """Модель элемента заказа"""
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    price_at_time = db.Column(db.Numeric(precision=10, scale=2), nullable=False)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    def __repr__(self):
        return f'<OrderItem Order:{self.order_id} Book:{self.book_id} Qty:{self.quantity}>'
    @property
    def total_price(self):
        """Общая стоимость элемента заказа"""
        return float(self.price_at_time) * self.quantity
    def to_dict(self):
        """Преобразование в словарь для JSON API"""
        return {
            'id': self.id,
            'quantity': self.quantity,
            'price_at_time': float(self.price_at_time),
            'total_price': self.total_price,
            'book': self.book.to_dict() if self.book else None,
            'created_at': self.created_at.isoformat()
        } 