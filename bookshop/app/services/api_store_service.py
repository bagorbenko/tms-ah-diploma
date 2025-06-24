import requests
from flask import current_app
from datetime import datetime

class ApiStoreService:
    """Сервис для интеграции с API Store"""
    
    def __init__(self):
        self.api_store_url = current_app.config.get('API_STORE_URL')
        self.timeout = 10
    
    def send_order(self, order):
        """Отправить заказ в API Store"""
        try:
            # Подготавливаем данные для API Store
            purchase_data = []
            for item in order.items:
                purchase_data.append({
                    'order_id': order.id,
                    'book_id': item.book_id,
                    'user_id': order.user_id,
                    'book_title': item.book.title,
                    'author_name': item.book.author.name,
                    'price': float(item.price_at_time) * item.quantity,
                    'create_at': datetime.now().strftime('%Y-%m-%d'),
                    'publisher_id': 1  # Заглушка для publisher_id
                })
            
            print(f'📦 Отправка заказа {order.order_number} в API Store: {self.api_store_url}')
            
            # Отправляем POST запрос
            response = requests.post(
                f'{self.api_store_url}/purchases/',
                json=purchase_data,
                timeout=self.timeout,
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code in [200, 201]:
                print(f'✅ Заказ успешно отправлен в API Store')
                return {
                    'status': 'sent',
                    'response': response.json(),
                    'http_status': response.status_code
                }
            else:
                print(f'⚠️ Ошибка отправки в API Store: HTTP {response.status_code}')
                return {
                    'status': 'failed',
                    'error': f'HTTP {response.status_code}',
                    'response_text': response.text[:500]  # Первые 500 символов ответа
                }
                
        except requests.exceptions.Timeout:
            print(f'⏰ Таймаут при отправке в API Store')
            return {
                'status': 'timeout',
                'error': 'Request timeout'
            }
        except requests.exceptions.ConnectionError:
            print(f'🔌 Ошибка соединения с API Store')
            return {
                'status': 'connection_error',
                'error': 'Connection error'
            }
        except Exception as e:
            print(f'❌ Неожиданная ошибка при отправке в API Store: {e}')
            return {
                'status': 'error',
                'error': str(e)
            }
    
    def check_connection(self):
        """Проверить соединение с API Store"""
        try:
            response = requests.get(f'{self.api_store_url}/', timeout=5)
            return response.status_code == 200
        except:
            return False 