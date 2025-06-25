"""
Вспомогательные функции для приложения
"""
import requests
import chardet


def fetch_html_with_encoding(url, timeout=10):
    """
    Загружает HTML с правильным определением кодировки
    
    Args:
        url (str): URL для загрузки
        timeout (int): Таймаут в секундах
        
    Returns:
        tuple: (content, status_code)
    """
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            # Попробуем определить кодировку автоматически
            detected = chardet.detect(response.content)
            encoding = detected.get('encoding', 'utf-8')
            
            # Принудительно используем UTF-8 для русского текста
            if encoding.lower() in ['windows-1251', 'cp1251', 'iso-8859-1']:
                encoding = 'utf-8'
            
            try:
                content = response.content.decode(encoding)
            except UnicodeDecodeError:
                # Если не получается декодировать, пробуем UTF-8
                content = response.content.decode('utf-8', errors='replace')
            
            return content, response.status_code
        else:
            return None, response.status_code
    except Exception as e:
        return None, 500


def ensure_utf8_headers():
    """
    Возвращает заголовки для правильной работы с UTF-8
    """
    return {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    } 