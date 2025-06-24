from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def health_check():
    return jsonify({
        'service': 'Bookshop',
        'status': 'healthy',
        'message': 'Simple Flask app working!'
    })

@app.route('/api/books')
def get_books():
    books = [
        {'id': 1, 'title': 'Чистый код', 'author': 'Роберт Мартин', 'price': 1500},
        {'id': 2, 'title': 'Архитектура ПО', 'author': 'Мартин Фаулер', 'price': 2000},
        {'id': 3, 'title': 'Python для профессионалов', 'author': 'Дэн Бейдер', 'price': 1800}
    ]
    return jsonify(books)

if __name__ == '__main__':
    print('🚀 Simple Bookshop запущен на порту 8000')
    app.run(host='0.0.0.0', port=8000, debug=False) 