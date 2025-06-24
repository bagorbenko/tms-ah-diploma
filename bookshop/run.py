#!/usr/bin/env python3
"""
Главный файл для запуска Flask приложения
"""
import os
from app import create_app

# Создаем приложение
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print(f'🚀 Запуск Flask Bookshop приложения на порту {port}')
    print(f'🔧 Debug режим: {debug}')
    print(f'🗄️ База данных: {app.config["SQLALCHEMY_DATABASE_URI"]}')
    print(f'🔗 API Store URL: {app.config["API_STORE_URL"]}')
    
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug
    ) 