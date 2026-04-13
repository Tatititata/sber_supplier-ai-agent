# Supplier AI Agent

Сервис для асинхронной обработки архивов с коммерческими предложениями.

## Как запустить проект

```bash
git clone https://github.com/Tatititata/sber_supplier-ai-agent.git
cd sber_supplier-ai-agent
docker compose up -d --build
```
Сервис будет доступен по адресу: `http://localhost:8000`  
Документация API: `http://localhost:8000/docs`

## Технологии

Python 3.12 — язык программирования  
FastAPI — веб-фреймворк  
PostgreSQL — база данных  
SQLAlchemy — ORM  
Alembic — миграции  
Docker — контейнеризация  
JWT — аутентификация  
Pytest — тестирование  

## Архитектура

app/main.py — эндпоинты API  
app/auth.py — JWT аутентификация и ролевая модель  
app/task_handler.py — бизнес-логика (создание задач, фоновя обработка, работа с БД)  
app/models.py — SQLAlchemy модели  
app/database.py — подключение к PostgreSQL  
tests/ — unit-тесты

Асинхронная обработка реализована через BackgroundTasks FastAPI. После загрузки файла задача сохраняется в БД со статусом pending, запускается фоновая обработка (имитация парсинга), статус меняется на processing, затем на completed или failed.


## Компромиссы

Парсинг данных заглушен случайной генерацией (имитация AI)  
Аутентификация использует in-memory словарь пользователей (в production заменить на БД)  
Фоновые задачи не сохраняются при перезапуске приложения

## Как проверить

#### Получить токен

```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user&password=userpassword"
```

#### Создать задачу

```bash
curl -X POST http://localhost:8000/cp/tasks \
  -H "Authorization: Bearer <token>" \
  -F "file=@test.zip"
```

#### Получить статус задачи

```bash
curl -X GET http://localhost:8000/cp/tasks/<task_id> \
  -H "Authorization: Bearer <token>"
```

## Запуск тестов

```bash
# Через Docker
docker compose run --rm app pytest tests/ -v

# Локально (требуется виртуальное окружение)
pytest tests/ -v
```

## Примеры запросов (curl)


#### 1. Получение токена

```bash
TOKEN=$(curl -s -X POST http://localhost:8000/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user&password=userpassword" | jq -r '.access_token')
```

#### 2. Создание задачи

```bash
RESPONSE=$(curl -s -X POST http://localhost:8000/cp/tasks \
  -H "Authorization: Bearer $TOKEN" \
  -F "file=@test.zip")
TASK_ID=$(echo $RESPONSE | jq -r '.task_id')
```

#### 3. Получение статуса

```bash
curl -s -X GET http://localhost:8000/cp/tasks/$TASK_ID \
  -H "Authorization: Bearer $TOKEN" | jq '.'
```