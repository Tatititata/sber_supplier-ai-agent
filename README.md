fastapi — создание API-эндпоинтов, валидация запросов, dependency injection.

uvicorn — ASGI-сервер для запуска FastAPI.

sqlalchemy — ORM для работы с PostgreSQL. Превращает Python-объекты в SQL-запросы и обратно.

asyncpg — асинхронный драйвер PostgreSQL. SQLAlchemy без него не подключится к базе.

alembic — миграции схемы БД.

python-multipart — FastAPI требует эту библиотеку для обработки загружаемых файлов (multipart/form-data). Без неё UploadFile не работает.

python-jose[cryptography] — создание и проверка JWT-токенов для аутентификации.

passlib[bcrypt] — хеширование паролей пользователей.

pytest — запуск unit-тестов.

pytest-asyncio — поддержка асинхронных тестов (pytest не умеет тестировать async-функции без этого).

httpx — HTTP-клиент для тестирования API (замена requests в асинхронном коде).





Инициализировать alembic: alembic init migrations

Настроить alembic.ini: раскомментировать и указать sqlalchemy.url = postgresql://agent:agent123@localhost:5432/supplier_agent

Настроить migrations/env.py: добавить импорт from app.models import Task и target_metadata = Base.metadata (импортировать Base из app.database)

Сгенерировать миграцию: alembic revision --autogenerate -m "create tasks table"