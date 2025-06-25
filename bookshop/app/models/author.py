from app import db
from datetime import datetime
class Author(db.Model):
    """Модель автора книги"""
    __tablename__ = 'authors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    bio = db.Column(db.Text)
    birth_date = db.Column(db.Date)
    nationality = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    books = db.relationship('Book', backref='author', lazy=True)
    def __repr__(self):
        return f'<Author {self.name}>'
    def to_dict(self):
        """Преобразование в словарь для JSON API"""
        return {
            'id': self.id,
            'name': self.name,
            'bio': self.bio,
            'birth_date': self.birth_date.isoformat() if self.birth_date else None,
            'nationality': self.nationality,
            'books_count': len(self.books),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        } 