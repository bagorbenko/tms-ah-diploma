from flask import Blueprint, request, jsonify
from app import db
from app.models.category import Category
from datetime import datetime
categories_bp = Blueprint('categories', __name__)
@categories_bp.route('/categories', methods=['GET'])
def get_categories():
    """Получить все категории"""
    try:
        categories = Category.query.all()
        return jsonify({
            'count': len(categories),
            'categories': [category.to_dict() for category in categories]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@categories_bp.route('/categories', methods=['POST'])
def create_category():
    """Создать категорию"""
    try:
        data = request.get_json()
        if not data or 'name' not in data:
            return jsonify({'error': 'Поле name обязательно'}), 400
        existing = Category.query.filter_by(name=data['name']).first()
        if existing:
            return jsonify({'error': 'Категория с таким именем уже существует'}), 400
        category = Category(
            name=data['name'],
            description=data.get('description')
        )
        db.session.add(category)
        db.session.commit()
        return jsonify({
            'message': 'Категория создана',
            'category': category.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@categories_bp.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Получить категорию по ID"""
    try:
        category = Category.query.get_or_404(category_id)
        return jsonify(category.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@categories_bp.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Обновить категорию"""
    try:
        category = Category.query.get_or_404(category_id)
        data = request.get_json()
        if 'name' in data and data['name'] != category.name:
            existing = Category.query.filter_by(name=data['name']).first()
            if existing:
                return jsonify({'error': 'Категория с таким именем уже существует'}), 400
        if 'name' in data:
            category.name = data['name']
        if 'description' in data:
            category.description = data['description']
        category.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({
            'message': 'Категория обновлена',
            'category': category.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@categories_bp.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Удалить категорию"""
    try:
        category = Category.query.get_or_404(category_id)
        if category.books:
            return jsonify({'error': 'Нельзя удалить категорию, в которой есть книги'}), 400
        db.session.delete(category)
        db.session.commit()
        return jsonify({'message': 'Категория удалена'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 