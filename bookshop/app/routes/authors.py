from flask import Blueprint, request, jsonify
from app import db
from app.models.author import Author
from datetime import datetime

authors_bp = Blueprint('authors', __name__)

@authors_bp.route('/authors', methods=['GET'])
def get_authors():
    """Получить всех авторов"""
    try:
        authors = Author.query.all()
        return jsonify({
            'count': len(authors),
            'authors': [author.to_dict() for author in authors]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@authors_bp.route('/authors', methods=['POST'])
def create_author():
    """Создать автора"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Поле name обязательно'}), 400
        
        author = Author(
            name=data['name'],
            bio=data.get('bio'),
            nationality=data.get('nationality'),
            birth_date=datetime.strptime(data['birth_date'], '%Y-%m-%d').date() if data.get('birth_date') else None
        )
        
        db.session.add(author)
        db.session.commit()
        
        return jsonify({
            'message': 'Автор создан',
            'author': author.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@authors_bp.route('/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    """Получить автора по ID"""
    try:
        author = Author.query.get_or_404(author_id)
        return jsonify(author.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@authors_bp.route('/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    """Обновить автора"""
    try:
        author = Author.query.get_or_404(author_id)
        data = request.get_json()
        
        if 'name' in data:
            author.name = data['name']
        if 'bio' in data:
            author.bio = data['bio']
        if 'nationality' in data:
            author.nationality = data['nationality']
        if 'birth_date' in data and data['birth_date']:
            author.birth_date = datetime.strptime(data['birth_date'], '%Y-%m-%d').date()
        
        author.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'message': 'Автор обновлен',
            'author': author.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@authors_bp.route('/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    """Удалить автора"""
    try:
        author = Author.query.get_or_404(author_id)
        
        if author.books:
            return jsonify({'error': 'Нельзя удалить автора, у которого есть книги'}), 400
        
        db.session.delete(author)
        db.session.commit()
        
        return jsonify({'message': 'Автор удален'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 