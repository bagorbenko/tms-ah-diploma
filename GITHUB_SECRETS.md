# GitHub Secrets для CI/CD Pipeline

Для корректной работы CI/CD pipeline необходимо настроить следующие секреты в GitHub:

## Секреты для Google Cloud Platform

### `GCP_SA_KEY`
JSON ключ сервисного аккаунта Google Cloud Platform.

**Как получить:**
1. Зайдите в [Google Cloud Console](https://console.cloud.google.com/)
2. Перейдите в IAM & Admin > Service Accounts
3. Создайте новый сервисный аккаунт или выберите существующий
4. Добавьте роли:
   - `Editor` (для управления ресурсами)
   - `Storage Admin` (для Terraform state)
   - `Kubernetes Engine Admin` (для GKE)
5. Создайте JSON ключ
6. Скопируйте содержимое JSON файла в секрет `GCP_SA_KEY`

**Пример формата:**
```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
```

## Секреты для Terraform

### `TF_STATE_BUCKET`
Имя Google Cloud Storage bucket для хранения Terraform state.

**Пример:** `your-project-terraform-state`

## Секреты для Kubernetes Deployment

### `GKE_CLUSTER`
Имя GKE кластера.

**Пример:** `your-cluster-name`

### `GKE_ZONE`
Зона/регион где развернут GKE кластер.

**Пример:** `europe-west3`

### `GCP_PROJECT`
ID проекта Google Cloud Platform.

**Пример:** `your-project-id-123456`

## Секреты для базы данных API Store

### `DB_API_HOST`
Хост базы данных для API Store.

### `DB_API_PORT`
Порт базы данных для API Store.

### `DB_API_NAME`
Имя базы данных для API Store.

### `DB_API_USER`
Пользователь базы данных для API Store.

### `DB_API_PASSWORD`
Пароль базы данных для API Store.

## Секреты для базы данных Bookshop

### `DB_BOOKSHOP_HOST`
Хост базы данных для Bookshop.

### `DB_BOOKSHOP_PORT`
Порт базы данных для Bookshop.

### `DB_BOOKSHOP_NAME`
Имя базы данных для Bookshop.

### `DB_BOOKSHOP_USER`
Пользователь базы данных для Bookshop.

### `DB_BOOKSHOP_PASSWORD`
Пароль базы данных для Bookshop.

## Как добавить секреты в GitHub

1. Перейдите в ваш репозиторий на GitHub
2. Settings > Secrets and variables > Actions
3. Нажмите "New repository secret"
4. Введите имя секрета и значение
5. Нажмите "Add secret"

## Проверка настройки

После добавления всех секретов, workflow должен успешно выполняться при push в ветки `main` или `develop`.

## Troubleshooting

### Ошибка "credentials is neither valid json nor a valid file path"

- Убедитесь что `GCP_SA_KEY` содержит корректный JSON
- Проверьте что JSON не содержит лишних пробелов или символов
- Убедитесь что сервисный аккаунт имеет необходимые права

### Ошибка подключения к базе данных

- Проверьте все секреты с префиксом `DB_`
- Убедитесь что база данных доступна из интернета (для production)
- Для тестов используется SQLite в памяти 