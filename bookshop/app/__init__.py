from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
db = SQLAlchemy()
migrate = Migrate()
def create_app(config_name=None):
    """Фабрика приложений Flask"""
    app = Flask(__name__)
    
    # Настройка кодировки по умолчанию
    app.config['JSON_AS_ASCII'] = False
    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
    else:
        database_url = os.getenv('DATABASE_URL', 'sqlite:///bookshop.db')
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['API_STORE_URL'] = os.getenv('API_STORE_URL', 'http://api-store-service.api-store-prod.svc.cluster.local')
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    from app.models import book, author, category, cart, order, user
    from app.routes.books import books_bp
    from app.routes.authors import authors_bp
    from app.routes.categories import categories_bp
    from app.routes.cart import cart_bp
    from app.routes.orders import orders_bp
    from app.routes.users import users_bp
    from app.routes.main import main_bp
    from app.routes.test_route import test_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(test_bp)  
    app.register_blueprint(books_bp, url_prefix='/api')
    app.register_blueprint(authors_bp, url_prefix='/api')
    app.register_blueprint(categories_bp, url_prefix='/api')
    app.register_blueprint(cart_bp, url_prefix='/api')
    app.register_blueprint(orders_bp, url_prefix='/api')
    app.register_blueprint(users_bp, url_prefix='/api')
    with app.app_context():
        db.create_all()
        if not app.config.get('TESTING', False):
            from app.services.data_seeder import seed_initial_data
            seed_initial_data()
    return app 