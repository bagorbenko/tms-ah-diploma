from app import db
from datetime import datetime
class Category(db.Model):
    """Модель категории книг"""
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True, index=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    books = db.relationship('Book', backref='category', lazy=True)
    def __repr__(self):
        return f'<Category {self.name}>'
    def to_dict(self):
        """Преобразование в словарь для JSON API"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'books_count': len(self.books),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 