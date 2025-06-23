# 🚀 Enterprise CI/CD Pipeline - Дипломный проект

## 📋 Обзор архитектуры

Этот проект реализует полноценный **Enterprise CI/CD Pipeline** для микросервисной архитектуры с использованием современных DevOps практик и инструментов.

### 🏗️ Архитектурная схема

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Development   │    │   Quality       │    │   Production    │
│   Environment   │    │   Assurance     │    │   Environment   │
│                 │    │   Environment   │    │                 │
│ • DEV Testing   │────│ • QA Testing    │────│ • Production    │
│ • Feature       │    │ • Integration   │    │ • Monitoring    │
│   Development   │    │ • Load Testing  │    │ • TLS Security  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 │
         ┌───────────────────────────────────────────────┐
         │          Enterprise CI/CD Pipeline            │
         │                                               │
         │ 1. Code Quality (SonarQube)                  │
         │ 2. Security Scanning (Snyk, OWASP ZAP)      │
         │ 3. Infrastructure as Code (Terraform)       │
         │ 4. Container Orchestration (Kubernetes)     │
         │ 5. Monitoring & Logging (Grafana)           │
         │ 6. Load Testing (k6)                        │
         │ 7. TLS Automation (cert-manager)            │
         └───────────────────────────────────────────────┘
```

## 🛠️ Технологический стек

### **Cloud & Infrastructure**
- **Google Cloud Platform (GKE)** - Container orchestration
- **Terraform** - Infrastructure as Code
- **Kubernetes** - Container orchestration
- **Docker** - Containerization

### **CI/CD & DevOps**
- **GitHub Actions** - CI/CD automation
- **SonarQube/SonarCloud** - Code quality analysis
- **Snyk** - Security vulnerability scanning
- **OWASP ZAP** - Security testing
- **k6** - Load testing

### **Monitoring & Observability**
- **Grafana** - Monitoring dashboards
- **Prometheus** - Metrics collection
- **Loki** - Log aggregation

### **Security & TLS**
- **cert-manager** - Automatic TLS certificate management
- **Let's Encrypt** - Free SSL certificates
- **Workload Identity** - Secure GKE authentication

## 🔄 Enterprise CI/CD Pipeline

### 1. **🚀 Инициализация и триггеры**
- Автоматический запуск при push в `main`, `develop`
- Ручной запуск через GitHub Actions UI
- Выбор среды развертывания (dev/qa/prod)

### 2. **🔨 Сборка приложений**
- Multi-stage Docker builds
- Кеширование слоев для оптимизации
- Сборка для каждого микросервиса параллельно
- Push в Google Container Registry

### 3. **🧪 Комплексное тестирование**
```bash
# Unit тесты
pytest --cov=app --cov-report=xml

# Integration тесты  
pytest tests/integration/

# Code coverage анализ
coverage report --show-missing
```

### 4. **📊 Анализ качества кода (SonarQube)**
- Статический анализ кода
- Проверка code coverage
- Обнаружение code smells
- Security hotspots
- Technical debt анализ

### 5. **🔒 Безопасность (DevSecOps)**
- **Snyk** - сканирование зависимостей
- **OWASP ZAP** - тестирование безопасности веб-приложений
- **Container scanning** - проверка Docker образов
- **DefectDojo** интеграция (опционально)

### 6. **🏗️ Инфраструктура как код**
```bash
# Инициализация Terraform
terraform init -backend-config="bucket=$TF_STATE_BUCKET"

# Планирование изменений
terraform plan -var="environment=prod"

# Применение изменений
terraform apply -auto-approve
```

### 7. **🚀 Развертывание приложений**
- Deployment в разные среды (dev/qa/prod)
- Blue-Green deployment стратегия
- Automatic rollback при сбоях
- Health checks и readiness probes

### 8. **🔐 Настройка TLS**
- Автоматическое получение SSL сертификатов
- Let's Encrypt интеграция
- Принудительное перенаправление на HTTPS
- Certificate rotation

### 9. **📊 Мониторинг и логирование**
- Grafana dashboards для визуализации
- Prometheus metrics collection
- Custom application metrics
- Alert management

### 10. **🏋️ Нагрузочное тестирование**
```javascript
// k6 load testing scenario
export let options = {
  stages: [
    { duration: '2m', target: 10 },
    { duration: '5m', target: 10 },
    { duration: '2m', target: 20 },
    { duration: '5m', target: 20 },
    { duration: '2m', target: 0 },
  ],
  thresholds: {
    http_req_duration: ['p(99)<1500'],
    http_req_failed: ['rate<0.1'],
  },
};
```

### 11. **🌐 Статический контент**
- Автоматическое развертывание в Cloud Storage
- CDN интеграция
- Versioning и cache invalidation

## 🎯 Развертывание по средам

### **Development Environment**
```bash
# Запуск DEV среды
git push origin feature/my-feature

# Или ручной запуск
gh workflow run enterprise-cicd.yml -f environment=dev
```

### **Quality Assurance Environment**
```bash
# Автоматический запуск при push в develop
git push origin develop

# Включает полное тестирование и QA проверки
```

### **Production Environment**
```bash
# Автоматический запуск при push в main
git push origin main

# С полным набором production security мер
```

## 🔧 Настройка проекта

### **1. GitHub Secrets**
Настройте следующие секреты в GitHub репозитории:

```bash
# Google Cloud
GCP_SA_KEY              # Service Account JSON key
GCP_PROJECT_ID          # Project ID

# SonarCloud
SONAR_TOKEN            # SonarCloud authentication token

# Snyk
SNYK_TOKEN             # Snyk API token

# Terraform
TF_STATE_BUCKET        # Bucket для Terraform state

# Database
DB_API_HOST            # API Store database host
DB_API_PORT            # API Store database port
DB_API_NAME            # API Store database name
DB_API_USER            # API Store database user
DB_API_PASSWORD        # API Store database password

DB_BOOKSHOP_HOST       # Bookshop database host
DB_BOOKSHOP_PORT       # Bookshop database port
DB_BOOKSHOP_NAME       # Bookshop database name
DB_BOOKSHOP_USER       # Bookshop database user
DB_BOOKSHOP_PASSWORD   # Bookshop database password
```

### **2. SonarCloud настройка**
1. Подключите репозиторий к SonarCloud
2. Создайте проект с ключом: `diploma-microservices`
3. Получите токен и добавьте в GitHub Secrets

### **3. Snyk настройка**
1. Зарегистрируйтесь в Snyk
2. Подключите GitHub репозиторий
3. Получите API токен

### **4. Terraform State**
```bash
# Создайте bucket для Terraform state
gsutil mb gs://your-terraform-state-bucket
gsutil versioning set on gs://your-terraform-state-bucket
```

## 🚀 Запуск развертывания

### **Локальная разработка**
```bash
# 1. Клонируйте репозиторий
git clone https://github.com/your-username/fullstack.git
cd fullstack

# 2. Настройте среду
cp .env.example .env
# Отредактируйте .env файл

# 3. Запустите локально
docker-compose up -d

# 4. Запустите тесты
docker-compose exec api-store pytest
docker-compose exec bookshop pytest
```

### **Cloud развертывание**
```bash
# 1. Настройте Terraform
cd terraform
terraform init
terraform plan -var="environment=dev"
terraform apply -var="environment=dev"

# 2. Настройте kubectl
gcloud container clusters get-credentials diploma-cluster-dev --region europe-west3

# 3. Разверните приложения
kubectl apply -f k8s/

# 4. Настройте мониторинг
helm repo add grafana https://grafana.github.io/helm-charts
helm install grafana grafana/grafana --values monitoring/grafana-values.yaml
```

## 📊 Мониторинг и дашборды

### **Grafana дашборды**
- **Application Overview** - общие метрики приложений
- **Kubernetes Cluster** - состояние кластера
- **Custom Microservices** - специфичные метрики проекта

### **Доступ к мониторингу**
```bash
# Получить пароль Grafana
kubectl get secret grafana -o jsonpath="{.data.admin-password}" | base64 --decode

# Port forward для доступа
kubectl port-forward svc/grafana 3000:80
```

### **Алерты и уведомления**
- Slack/Teams интеграция
- Email уведомления
- PagerDuty для критических алертов

## 🔒 Безопасность

### **Network Security**
- VPC-native networking
- Network policies
- Private cluster endpoints (production)

### **Identity & Access Management**
- Workload Identity для pod'ов
- Service accounts с минимальными правами
- RBAC для Kubernetes

### **Container Security**
- Vulnerability scanning
- Binary Authorization (production)
- Security contexts
- Non-root containers

## 📈 Масштабирование

### **Horizontal Pod Autoscaler**
```yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: api-store-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: api-store-deployment
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### **Cluster Autoscaler**
- Автоматическое масштабирование узлов
- Preemptible instances для dev/qa
- Dedicated instances для production

## 🎓 Демонстрация на защите диплома

### **Что показать:**
1. **CI/CD Pipeline** - полный цикл от коммита до production
2. **Multi-environment** развертывание
3. **Security scanning** результаты
4. **Load testing** результаты
5. **Monitoring dashboards** в Grafana
6. **Infrastructure as Code** с Terraform

### **Ключевые моменты:**
- ✅ **DevSecOps** подход с интегрированной безопасностью
- ✅ **Infrastructure as Code** для воспроизводимости
- ✅ **Multi-stage pipeline** с quality gates
- ✅ **Automated testing** на всех уровнях
- ✅ **Production-ready** конфигурации
- ✅ **Monitoring & Observability** из коробки

## 📞 Поддержка

Для вопросов по развертыванию и настройке создайте issue в репозитории или обратитесь к документации конкретных компонентов.

---
**Enterprise CI/CD Pipeline готов к демонстрации и production использованию! 🚀** 