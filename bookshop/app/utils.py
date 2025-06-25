import requests
import chardet


def fetch_html_with_encoding(url, timeout=10):
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            detected = chardet.detect(response.content)
            encoding = detected.get('encoding', 'utf-8')
            
            if encoding.lower() in ['windows-1251', 'cp1251', 'iso-8859-1']:
                encoding = 'utf-8'
            
            try:
                content = response.content.decode(encoding)
            except UnicodeDecodeError:
                content = response.content.decode('utf-8', errors='replace')
            
            return content, response.status_code
        else:
            return None, response.status_code
    except Exception as e:
        return None, 500


def ensure_utf8_headers():
    return {
        'Content-Type': 'text/html; charset=utf-8',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
    } 