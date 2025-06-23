# 🦆 DuckDNS + SSL Setup Guide

## 📋 Обзор

Этот гид поможет вам настроить **бесплатные SSL сертификаты** для вашего дипломного проекта используя:
- **DuckDNS** - бесплатный динамический DNS сервис
- **Let's Encrypt** - бесплатные SSL сертификаты
- **cert-manager** - автоматическое управление сертификатами в Kubernetes

## 🌟 Преимущества DuckDNS

- ✅ **Бесплатно навсегда**
- ✅ **Простая настройка** - без регистрации доменов
- ✅ **Автоматическое обновление** IP адресов
- ✅ **Поддержка SSL** сертификатов
- ✅ **Идеально для демонстрации** проектов

## 🚀 Быстрый старт

### 1. Регистрация в DuckDNS

1. Перейдите на https://www.duckdns.org/
2. Войдите через один из провайдеров (Google, GitHub, etc.)
3. Создайте домен, например: `diploma-project`
4. Скопируйте ваш **токен** с главной страницы

### 2. Настройка GitHub Secrets

Добавьте в GitHub Secrets:
```bash
DUCKDNS_TOKEN=your-duckdns-token-here
DUCKDNS_DOMAIN=diploma-project  # без .duckdns.org
```

### 3. Автоматическая настройка через CI/CD

При развертывании в production среду, наш CI/CD pipeline автоматически:
- Настроит DuckDNS домены
- Установит cert-manager
- Получит SSL сертификаты
- Настроит HTTPS редиректы

## 🛠️ Ручная настройка

### Шаг 1: Подключитесь к кластеру
```bash
gcloud container clusters get-credentials diploma-cluster-prod --region europe-west3
```

### Шаг 2: Запустите скрипт настройки
```bash
# Установите переменные окружения
export DUCKDNS_TOKEN="your-token-here"
export DUCKDNS_DOMAIN="diploma-project"
export ENVIRONMENT="prod"

# Запустите скрипт
chmod +x scripts/setup-duckdns.sh
./scripts/setup-duckdns.sh
```

### Шаг 3: Установите cert-manager
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Дождитесь готовности
kubectl wait --for=condition=ready pod -l app.kubernetes.io/name=cert-manager -n cert-manager --timeout=300s
```

### Шаг 4: Настройте SSL сертификаты
```bash
kubectl apply -f k8s/tls-certificates.yaml
```

### Шаг 5: Проверьте статус сертификатов
```bash
# Проверьте сертификаты
kubectl get certificates -A

# Подробная информация
kubectl describe certificates -A

# Логи cert-manager
kubectl logs -n cert-manager -l app.kubernetes.io/name=cert-manager
```

## 🌐 Ваши домены

После настройки у вас будут следующие HTTPS домены:

| Сервис | URL | Описание |
|--------|-----|----------|
| **Main** | `https://diploma-project.duckdns.org` | Главная страница |
| **API Store** | `https://api-diploma-project.duckdns.org` | FastAPI сервис |
| **Bookshop** | `https://bookshop-diploma-project.duckdns.org` | Django сервис |
| **Grafana** | `https://grafana-diploma-project.duckdns.org` | Мониторинг |

## 🔄 Автоматическое обновление IP

Наш **DuckDNS Updater** автоматически:
- Проверяет IP адреса LoadBalancer сервисов каждые 5 минут
- Обновляет DuckDNS записи при изменении IP
- Логирует все операции для отладки

### Проверка статуса updater'а:
```bash
# Статус CronJob
kubectl get cronjob duckdns-updater -n kube-system

# Логи последнего запуска
kubectl logs -l job-name=duckdns-updater -n kube-system --tail=50

# Ручной запуск для тестирования
kubectl create job --from=cronjob/duckdns-updater manual-duckdns-update -n kube-system
```

## 🔐 SSL Сертификаты

### Автоматическое получение
- **Let's Encrypt** автоматически выдает сертификаты
- **cert-manager** управляет жизненным циклом
- **Автообновление** за 30 дней до истечения

### Проверка SSL:
```bash
# Онлайн проверка
curl -I https://api-diploma-project.duckdns.org

# Детали сертификата
openssl s_client -connect api-diploma-project.duckdns.org:443 -servername api-diploma-project.duckdns.org < /dev/null 2>/dev/null | openssl x509 -text -noout
```

## 🐛 Troubleshooting

### Проблема: DNS не обновляется
```bash
# Проверьте токен DuckDNS
kubectl get secret duckdns-secret -n kube-system -o yaml

# Проверьте логи updater'а
kubectl logs -l job-name=duckdns-updater -n kube-system

# Ручное обновление
curl "https://www.duckdns.org/update?domains=diploma-project&token=YOUR_TOKEN&ip=YOUR_IP"
```

### Проблема: SSL сертификат не выдается
```bash
# Проверьте статус cert-manager
kubectl get pods -n cert-manager

# Проверьте ClusterIssuer
kubectl get clusterissuer

# Проверьте challenges
kubectl get challenges -A

# Логи cert-manager
kubectl logs -n cert-manager -l app.kubernetes.io/name=cert-manager
```

### Проблема: Ingress не работает
```bash
# Проверьте Ingress controller
kubectl get pods -n ingress-nginx

# Если нет, установите:
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml

# Проверьте Ingress ресурсы
kubectl get ingress -A
```

## 📊 Мониторинг SSL

### Grafana Dashboard для SSL
Добавьте метрики для мониторинга SSL сертификатов:

```yaml
# В Prometheus scrape config
- job_name: 'ssl-exporter'
  static_configs:
  - targets:
    - api-diploma-project.duckdns.org:443
    - bookshop-diploma-project.duckdns.org:443
    - grafana-diploma-project.duckdns.org:443
  metrics_path: /probe
  params:
    module: [https_2xx]
```

### Алерты на истечение сертификатов
```yaml
groups:
- name: ssl-expiry
  rules:
  - alert: SSLCertExpiringSoon
    expr: probe_ssl_earliest_cert_expiry - time() < 86400 * 7
    for: 1h
    labels:
      severity: warning
    annotations:
      summary: "SSL certificate expires soon"
      description: "SSL certificate for {{ $labels.instance }} expires in less than 7 days"
```

## 🎯 Для демонстрации диплома

### Что показать:
1. **Автоматическое получение SSL** - покажите как cert-manager получает сертификаты
2. **HTTPS редиректы** - покажите что HTTP автоматически перенаправляется на HTTPS
3. **Валидные сертификаты** - покажите зеленый замок в браузере
4. **Автообновление DNS** - покажите как система обновляет IP при изменениях

### Команды для демонстрации:
```bash
# Показать все сертификаты
kubectl get certificates -A

# Показать статус DuckDNS updater
kubectl get cronjob duckdns-updater -n kube-system

# Проверить SSL в браузере
echo "Откройте https://api-diploma-project.duckdns.org в браузере"

# Показать автоматические редиректы
curl -I http://api-diploma-project.duckdns.org
```

## 🔗 Полезные ссылки

- [DuckDNS Official Site](https://www.duckdns.org/)
- [Let's Encrypt](https://letsencrypt.org/)
- [cert-manager Documentation](https://cert-manager.io/docs/)
- [SSL Labs Test](https://www.ssllabs.com/ssltest/)

## 💡 Советы

1. **Используйте staging сертификаты** для тестирования (избегайте rate limits)
2. **Проверяйте DNS propagation** перед получением сертификатов
3. **Мониторьте срок действия** сертификатов
4. **Делайте backup** важных секретов

---

## 🎉 Результат

После настройки у вас будет:
- ✅ **Бесплатные HTTPS домены** для всех сервисов
- ✅ **Автоматическое обновление** DNS и SSL
- ✅ **Production-ready** конфигурация
- ✅ **Готовность к демонстрации** на защите диплома

**Ваш проект теперь доступен по HTTPS! 🔐✨** 