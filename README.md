### Приветсвую! Очень не против дописать где-то начатые док стринг, свэгер сделать читабельным или даже написать деплой на докерхаб - к сожалению поджало время.

## Структура проекта
  ```bash
   app/
      api/           # эндпоинты
      core/          # конфигурация, база, инициализация
      crud/          # логика работы с базой
      models/        # SQLAlchemy модели
      schemas/       # Pydantic схемы
      services/      # логика
      utils/.        # вспомогательные функции
      main.py        # точка входа
  ```

## Технологии

- **Python 3.9**
- **FastAPI**
- **SQLAlchemy**
- **SQLite**
- **Alembic**
- **Pydantic**
- **Uvicorn**

## Запуск

1. Клонирование репозитория:

   ```bash
   git clone git@github.com:LevKorobeinikov/test_taks_for_ITWorld.git
   cd test_taks_for_ITWorld
   ```

2. Создать и активировать виртуальное окружение:

   Для Windows:

   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```

   Для Linux/macOS:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. Установка зависимостей:
   ```bach
   pip install -r requirements.txt
   ```
4. Создайте файл с переменными окружения .env. Укажите в файле значения локальных переменных, представленных в образце .env.example
   ```bach
   cd app/
   touch .env
   ```
5. Примените миграции и запустите проект.
   ```bach
   alembic upgrade
   uvicorn app.main:app --reload
   # для новых миграций - alembic revision --autogenerate -m 'описание изменений'
   ```

## Запуск через докер

1. Соберите образ
   ```bach
   docker build -t myfastapi .
   ```
2. Запустите контейнер с пробросом порта
   ```bach
   docker run -p 8000:8000 myfastapi
   ```

## Доступ к стартовой страние и  документации 
[Стартовая сраница](http://localhost:8000)
1. [Swagger](http://localhost:8000/docs)
2. [ReDoc](http://localhost:8000/redoc)

## Автор  - [Коробейников Лев Сергеевич](https://github.com/LevKorobeinikov)
