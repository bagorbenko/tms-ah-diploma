from app import db
from datetime import datetime

class CartItem(db.Model):
    """Модель элемента корзины"""
    __tablename__ = 'cart_items'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Внешние ключи
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'), nullable=False)
    
    # Уникальность: один пользователь может иметь только один элемент для каждой книги
    __table_args__ = (db.UniqueConstraint('user_id', 'book_id', name='unique_user_book_cart'),)
    
    def __repr__(self):
        return f'<CartItem User:{self.user_id} Book:{self.book_id} Qty:{self.quantity}>'
    
    @property
    def total_price(self):
        """Общая стоимость элемента корзины"""
        return float(self.book.price) * self.quantity if self.book else 0
    
    def to_dict(self):
        """Преобразование в словарь для JSON API"""
        return {
            'id': self.id,
            'quantity': self.quantity,
            'total_price': self.total_price,
            'book': self.book.to_dict() if self.book else None,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 