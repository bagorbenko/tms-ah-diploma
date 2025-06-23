# 🎓 Дипломный проект: Интеграция микросервисов в облачной среде

## Структура репозитория

```
fullstack/
├── diploma-project/             # 🎯 ОСНОВНОЙ ДИПЛОМНЫЙ ПРОЕКТ
│   ├── services/               # Микросервисы
│   │   ├── bookshop/          # Django приложение (полная версия)
│   │   ├── api-store/         # FastAPI приложение (полная версия)
│   │   ├── simple-bookshop.py # Упрощенная версия для демо
│   │   └── simple-api-store.py# Упрощенная версия для демо
│   ├── deployment/            # Конфигурации развертывания
│   │   ├── kubernetes/        # K8s манифесты
│   │   └── docker/           # Dockerfile'ы
│   ├── frontend/             # Веб-интерфейсы
│   │   ├── cloud-frontend.html   # Продакшн версия
│   │   └── demo-frontend.html    # Демо версия
│   ├── tests/                # Тесты
│   ├── docs/                 # Документация
│   │   ├── ARCHITECTURE.md   # Описание архитектуры
│   │   └── DEPLOYMENT.md     # Руководство по развертыванию
│   └── README.md             # Основная документация проекта
├── bookshop/                 # Исходные файлы (для справки)
├── api-store/               # Исходные файлы (для справки)
├── k8s/                     # Kubernetes конфигурации (актуальные)
├── terraform/               # Terraform конфигурации
└── README.md               # Этот файл
```

## 🚀 Быстрый старт

### Для демонстрации диплома:

1. **Перейти в папку проекта:**
   ```bash
   cd diploma-project
   ```

2. **Запустить локальную демонстрацию:**
   ```bash
   # Terminal 1: API Store
   python services/simple-api-store.py
   
   # Terminal 2: Bookshop  
   python services/simple-bookshop.py
   
   # Terminal 3: Frontend
   python -m http.server 8080
   ```

3. **Открыть демо в браузере:**
   ```
   http://localhost:8080/frontend/demo-frontend.html
   ```

### Для облачного развертывания:

1. **Развернуть в Kubernetes:**
   ```bash
   kubectl apply -f k8s/
   ```

2. **Открыть облачный фронтенд:**
   ```bash
   python -m http.server 8081
   # Открыть: http://localhost:8081/diploma-project/frontend/cloud-frontend.html
   ```

## 📋 Описание проекта

Данный дипломный проект демонстрирует:

### Технологии:
- **Backend:** Django REST Framework + FastAPI
- **Frontend:** HTML5/CSS3/JavaScript (Vanilla)
- **DevOps:** Docker + Kubernetes + Google Cloud Platform
- **Integration:** HTTP REST API

### Архитектура:
- **Микросервисная архитектура** с двумя независимыми сервисами
- **Автоматическая интеграция** между сервисами
- **Облачное развертывание** в GCP
- **Отказоустойчивость** с fallback режимами

### Ключевые особенности:
1. ✅ Реальная интеграция микросервисов
2. ✅ Облачное развертывание (GKE)
3. ✅ Современный UI с визуализацией интеграции
4. ✅ Полная документация и тесты
5. ✅ Готовые Docker образы
6. ✅ Kubernetes манифесты

## 🎯 Цели проекта

1. **Демонстрация микросервисной архитектуры**
2. **Практическое применение DevOps практик**
3. **Интеграция современных облачных технологий**
4. **Создание production-ready решения**

## 📚 Документация

Вся подробная документация находится в папке `diploma-project/`:

- **[README.md](diploma-project/README.md)** - Основное описание проекта
- **[docs/ARCHITECTURE.md](diploma-project/docs/ARCHITECTURE.md)** - Архитектура системы
- **[docs/DEPLOYMENT.md](diploma-project/docs/DEPLOYMENT.md)** - Руководство по развертыванию

## 🧪 Тестирование

```bash
cd diploma-project
python tests/test_integration_k8s.py
```

## 📊 Результаты

### Достигнутые цели:
- [x] Создана микросервисная архитектура
- [x] Реализована автоматическая интеграция
- [x] Развернуто в облачной среде (GCP)
- [x] Создан современный пользовательский интерфейс
- [x] Написаны интеграционные тесты
- [x] Создана полная документация

### Технические достижения:
- Использование современного стека технологий
- Реализация DevOps best practices
- Обеспечение отказоустойчивости системы
- Автоматизация процессов развертывания

---

## 🔗 Полезные ссылки

- **Внешние IP сервисов в GCP:**
  - Bookshop: http://35.246.145.95
  - API Store: http://34.40.126.3

- **Локальные адреса для разработки:**
  - Bookshop: http://localhost:8000
  - API Store: http://localhost:5050
  - Frontend: http://localhost:8080

---

**Автор:** [Ваше имя]  
**Год:** 2025  
**Учебное заведение:** [Название]  
**Тема:** Интеграция микросервисов в облачной среде 