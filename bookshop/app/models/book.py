from app import db
from datetime import datetime

class Book(db.Model):
    """Модель книги"""
    __tablename__ = 'books'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False, index=True)
    isbn = db.Column(db.String(20), unique=True, index=True)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    description = db.Column(db.Text)
    pages = db.Column(db.Integer)
    publication_date = db.Column(db.Date)
    stock_quantity = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(255))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Внешние ключи
    author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    
    # Связи
    cart_items = db.relationship('CartItem', backref='book', lazy=True, cascade='all, delete-orphan')
    order_items = db.relationship('OrderItem', backref='book', lazy=True)
    
    def __repr__(self):
        return f'<Book {self.title}>'
    
    @property
    def is_in_stock(self):
        """Проверка наличия на складе"""
        return self.stock_quantity > 0 and self.is_available
    
    def to_dict(self, include_relations=False):
        """Преобразование в словарь для JSON API"""
        data = {
            'id': self.id,
            'title': self.title,
            'isbn': self.isbn,
            'price': float(self.price) if self.price else 0,
            'description': self.description,
            'pages': self.pages,
            'publication_date': self.publication_date.isoformat() if self.publication_date else None,
            'stock_quantity': self.stock_quantity,
            'image_url': self.image_url,
            'is_available': self.is_available,
            'is_in_stock': self.is_in_stock,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
        
        if include_relations:
            data.update({
                'author': self.author.to_dict() if self.author else None,
                'category': self.category.to_dict() if self.category else None
            })
        else:
            data.update({
                'author_id': self.author_id,
                'category_id': self.category_id,
                'author_name': self.author.name if self.author else None,
                'category_name': self.category.name if self.category else None
            })
        
        return data 