# Diploma Project - Enterprise Microservices Platform

> Полнофункциональная система микросервисов с CI/CD, мониторингом и облачным развертыванием

[![CI/CD Pipeline](https://github.com/bagorbenko/tms-ah-diploma/actions/workflows/enterprise-cicd.yml/badge.svg)](https://github.com/bagorbenko/tms-ah-diploma/actions)
[![Kubernetes](https://img.shields.io/badge/Kubernetes-1.32-blue.svg)](https://kubernetes.io/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue.svg)](https://docker.com/)
[![GCP](https://img.shields.io/badge/GCP-Deployed-green.svg)](https://cloud.google.com/)

## Содержание

- [Архитектура](#архитектура)
- [Быстрый старт](#быстрый-старт)
- [Доступ к сервисам](#доступ-к-сервисам)
- [Локальная разработка](#локальная-разработка)
- [Облачное развертывание](#облачное-развертывание)
- [Мониторинг](#мониторинг)
- [Безопасность](#безопасность)
- [Тестирование](#тестирование)
- [API Документация](#api-документация)
- [Разработка](#разработка)

## Архитектура

### Обзор системы

Проект представляет собой микросервисную архитектуру, состоящую из двух основных сервисов:

- **Bookshop Service** - интернет-магазин книг на Flask
- **API Store Service** - сервис аналитики на FastAPI

### Технологический стек

#### Backend Services
- **Bookshop Service**: Flask 3.0.0, PostgreSQL, SQLAlchemy
- **API Store Service**: FastAPI 0.104.0, PostgreSQL, Pydantic v2

#### Frontend
- **HTML5/CSS3/JavaScript**: Responsive веб-интерфейсы
- **Bootstrap 5**: UI компоненты
- **Chart.js**: Графики и аналитика

#### Infrastructure
- **Kubernetes**: Оркестрация контейнеров (GKE)
- **Docker**: Контейнеризация
- **PostgreSQL**: Основная база данных
- **NGINX**: Reverse proxy и load balancing

#### DevOps & Monitoring
- **GitHub Actions**: CI/CD pipeline
- **Grafana**: Мониторинг и дашборды
- **Terraform**: Infrastructure as Code
- **Google Cloud Platform**: Облачная платформа

## Быстрый старт

### Предварительные требования

- Docker и Docker Compose
- kubectl (для Kubernetes)
- Google Cloud SDK (для облачного развертывания)
- Git

### Локальный запуск

```bash
# Клонирование репозитория
git clone https://github.com/bagorbenko/tms-ah-diploma.git
cd tms-ah-diploma

# Запуск с Docker Compose
docker-compose up -d

# Проверка статуса
docker-compose ps

# Доступ к сервисам
echo "Bookshop: http://localhost:8000"
echo "API Store: http://localhost:5050"
echo "Frontend: http://localhost:3000"
```

### Облачное развертывание

```bash
# Настройка GCP
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Развертывание через CI/CD
git push origin main
# Pipeline автоматически развернет все сервисы
```

## Доступ к сервисам

### Production Environment

| Сервис | URL | Описание |
|--------|-----|----------|
| **Bookshop** | [http://35.241.155.121](http://35.241.155.121) | Основной магазин книг |
| **API Store** | [http://130.211.61.44](http://130.211.61.44) | Analytics API |
| **Grafana** | [http://34.76.217.129:32743](http://34.76.217.129:32743) | Мониторинг |
| **Dashboard** | [Monitoring Dashboard](https://storage.googleapis.com/diploma-static-prod-645ba250/monitoring-dashboard.html) | Обзор системы |

### DuckDNS Domains

| Домен | Сервис | Status |
|-------|--------|--------|
| [bookshop-diploma-project.duckdns.org](http://bookshop-diploma-project.duckdns.org) | Bookshop | Active |
| [api-diploma-project.duckdns.org](http://api-diploma-project.duckdns.org) | API Store | Active |
| [grafana-diploma-project.duckdns.org:32743](http://grafana-diploma-project.duckdns.org:32743) | Grafana | Active |

### Local Development

| Сервис | URL | Порт |
|--------|-----|------|
| Bookshop | http://localhost:8000 | 8000 |
| API Store | http://localhost:5050 | 5050 |
| Frontend | http://localhost:3000 | 3000 |
| PostgreSQL (Bookshop) | localhost:5432 | 5432 |
| PostgreSQL (API Store) | localhost:5433 | 5433 |

## Локальная разработка

### Структура проекта

```
fullstack/
├── api-store/                 # FastAPI сервис
│   ├── app/                   # Основной код приложения
│   ├── migrations/            # Alembic миграции
│   ├── Dockerfile            # Docker конфигурация
│   └── requirements.txt      # Python зависимости
├── bookshop/                 # Flask сервис
│   ├── app/                  # Основной код приложения
│   ├── migrations/           # Flask-Migrate миграции
│   ├── Dockerfile           # Docker конфигурация
│   └── requirements.txt     # Python зависимости
├── k8s/                     # Kubernetes манифесты
│   ├── api-store-deployment.yaml
│   ├── bookshop-deployment.yaml
│   ├── grafana-final.yaml
│   └── tls-certificates.yaml
├── terraform/               # Infrastructure as Code
├── .github/workflows/       # CI/CD pipeline
├── docker-compose.yml       # Локальная разработка
└── monitoring-dashboard.html # Мониторинг интерфейс
```

### Разработка сервисов

#### Bookshop Service (Flask)

```bash
cd bookshop
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Запуск в режиме разработки
export FLASK_ENV=development
python run.py
```

#### API Store Service (FastAPI)

```bash
cd api-store
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Запуск в режиме разработки
uvicorn app.main:app --reload --host 0.0.0.0 --port 5050
```

### База данных

```bash
# Создание и применение миграций для Bookshop
cd bookshop
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Создание и применение миграций для API Store
cd api-store
alembic init alembic
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Облачное развертывание

### Terraform Infrastructure

```bash
# Инициализация Terraform
cd terraform
terraform init

# Планирование развертывания
terraform plan -var="environment=prod"

# Применение изменений
terraform apply -var="environment=prod"
```

### Kubernetes Deployment

```bash
# Применение манифестов
kubectl apply -f k8s/

# Проверка статуса деплоя
kubectl get pods -n bookshop-prod
kubectl get pods -n api-store-prod

# Просмотр логов
kubectl logs -f deployment/bookshop-deployment -n bookshop-prod
kubectl logs -f deployment/api-store-deployment -n api-store-prod
```

## Мониторинг

### Grafana Dashboard

Доступ к Grafana:
- URL: http://34.76.217.129:32743
- Логин: admin
- Пароль: diploma-2025

### Доступные метрики

- CPU и память использование
- Количество запросов
- Время ответа
- Статус сервисов
- Ошибки и исключения

### Логирование

```bash
# Просмотр логов приложений
kubectl logs -f deployment/bookshop-deployment -n bookshop-prod
kubectl logs -f deployment/api-store-deployment -n api-store-prod

# Просмотр логов инфраструктуры
kubectl logs -f deployment/grafana -n monitoring-prod
```

## Безопасность

### Аутентификация и авторизация

- JWT токены для API аутентификации
- RBAC в Kubernetes
- Сетевые политики для изоляции сервисов

### Сканирование безопасности

```bash
# Сканирование Docker образов
docker scout cves api-store:latest
docker scout cves bookshop:latest

# Аудит зависимостей Python
pip audit
```

## Тестирование

### Юнит тесты

```bash
# Тестирование Bookshop
cd bookshop
pytest tests/ -v --cov=app

# Тестирование API Store
cd api-store
pytest tests/ -v --cov=app
```

### Интеграционные тесты

```bash
# Запуск полного набора тестов
docker-compose -f docker-compose.test.yml up --abort-on-container-exit
```

### Нагрузочное тестирование

```bash
# K6 нагрузочные тесты
k6 run tests/load-test.js
```

## API Документация

### Bookshop Service

- Swagger UI: http://localhost:8000/api/docs
- OpenAPI JSON: http://localhost:8000/api/openapi.json

### API Store Service

- FastAPI Docs: http://localhost:5050/docs
- ReDoc: http://localhost:5050/redoc
- OpenAPI JSON: http://localhost:5050/openapi.json

### Основные эндпоинты

#### Bookshop API

```
GET    /api/books          # Получить все книги
POST   /api/books          # Создать книгу
GET    /api/books/{id}     # Получить книгу по ID
PUT    /api/books/{id}     # Обновить книгу
DELETE /api/books/{id}     # Удалить книгу

GET    /api/authors        # Получить всех авторов
GET    /api/categories     # Получить все категории
GET    /api/orders         # Получить заказы
POST   /api/orders         # Создать заказ
```

#### API Store

```
GET    /purchases          # Получить все покупки
POST   /purchases          # Создать покупку
GET    /purchases/{id}     # Получить покупку по ID
GET    /most-popular-day   # Самый популярный день
GET    /purchases/total-count # Общее количество книг
```

## Разработка

### Стандарты кода

- **Python**: PEP 8, Black formatter
- **JavaScript**: ESLint, Prettier
- **Документация**: Docstrings для всех функций

### Git Workflow

```bash
# Создание feature ветки
git checkout -b feature/new-feature

# Коммит изменений
git add .
git commit -m "Add new feature"

# Push и создание PR
git push origin feature/new-feature
```

### CI/CD Pipeline

Pipeline включает 11 этапов:

1. **Initialize** - Инициализация и настройка окружения
2. **Build** - Сборка Docker образов
3. **Test** - Юнит и интеграционные тесты
4. **Code Quality** - Анализ качества кода
5. **Security** - Сканирование безопасности
6. **Infrastructure** - Terraform развертывание
7. **Deploy** - Развертывание в Kubernetes
8. **Integration Tests** - Интеграционные тесты
9. **Performance Tests** - Тесты производительности
10. **Monitoring Setup** - Настройка мониторинга
11. **Notification** - Уведомления о статусе

### Настройка окружения разработки

```bash
# Установка зависимостей разработки
pip install -r requirements.dev.txt

# Настройка pre-commit hooks
pre-commit install

# Запуск линтеров
flake8 .
black .
isort .
```

## Устранение неполадок

### Частые проблемы

#### Проблемы с базой данных

```bash
# Проверка подключения к PostgreSQL
kubectl exec -it postgres-pod -- psql -U username -d database_name

# Восстановление базы данных
kubectl exec -i postgres-pod -- psql -U username -d database_name < backup.sql
```

#### Проблемы с сетью

```bash
# Проверка сетевой связности
kubectl exec -it pod-name -- nslookup service-name

# Проверка сетевых политик
kubectl get networkpolicies -A
```

#### Проблемы с ресурсами

```bash
# Проверка использования ресурсов
kubectl top nodes
kubectl top pods -A

# Масштабирование сервисов
kubectl scale deployment bookshop-deployment --replicas=3
```

### Логи и отладка

```bash
# Детальные логи
kubectl logs -f deployment/service-name --previous

# События кластера
kubectl get events --sort-by=.metadata.creationTimestamp

# Описание ресурсов
kubectl describe pod pod-name
```

## Лицензия

MIT License - см. файл [LICENSE](LICENSE) для деталей.

## Контакты

- Автор: [bagorbenko](https://github.com/bagorbenko)
- Email: bagorbenko@example.com
- Проект: [GitHub Repository](https://github.com/bagorbenko/tms-ah-diploma)

---

**Версия документации**: 2.0  
**Последнее обновление**: 2025-01-01
