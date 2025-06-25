from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User
from datetime import datetime
users_bp = Blueprint('users', __name__)
@users_bp.route('/users', methods=['GET'])
def get_users():
    """Получить всех пользователей"""
    try:
        users = User.query.all()
        return jsonify({
            'count': len(users),
            'users': [user.to_dict() for user in users]
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@users_bp.route('/users', methods=['POST'])
def create_user():
    """Создать пользователя"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Нет данных в запросе'}), 400
        required_fields = ['username', 'email']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Поле {field} обязательно'}), 400
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'Пользователь с таким именем уже существует'}), 400
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Пользователь с таким email уже существует'}), 400
        user = User(
            username=data['username'],
            email=data['email'],
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            phone=data.get('phone'),
            address=data.get('address')
        )
        if 'password' in data:
            user.set_password(data['password'])
        db.session.add(user)
        db.session.commit()
        return jsonify({
            'message': 'Пользователь создан',
            'user': user.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@users_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Получить пользователя по ID"""
    try:
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict(include_sensitive=True))
    except Exception as e:
        return jsonify({'error': str(e)}), 500
@users_bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Обновить пользователя"""
    try:
        user = User.query.get_or_404(user_id)
        data = request.get_json()
        if 'username' in data and data['username'] != user.username:
            if User.query.filter_by(username=data['username']).first():
                return jsonify({'error': 'Пользователь с таким именем уже существует'}), 400
        if 'email' in data and data['email'] != user.email:
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'error': 'Пользователь с таким email уже существует'}), 400
        updatable_fields = ['username', 'email', 'first_name', 'last_name', 'phone', 'address', 'is_active']
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
        if 'password' in data:
            user.set_password(data['password'])
        user.updated_at = datetime.utcnow()
        db.session.commit()
        return jsonify({
            'message': 'Пользователь обновлен',
            'user': user.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
@users_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Удалить пользователя"""
    try:
        user = User.query.get_or_404(user_id)
        if user.orders:
            return jsonify({'error': 'Нельзя удалить пользователя, у которого есть заказы'}), 400
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'Пользователь удален'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500 