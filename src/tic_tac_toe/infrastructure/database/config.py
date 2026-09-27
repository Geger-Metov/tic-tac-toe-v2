import os


def get_database_url() -> str:
    """
    Возвращает connection string для подключения к PostgreSQL.

    В Docker (см. compose.yaml) переменная DATABASE_URL приходит уже готовая:
        postgresql+asyncpg://user:password@db:5432/ttt_db

    Если запускаешь приложение локально (не в контейнере) и DATABASE_URL не задана,
    собираем строку из отдельных POSTGRES_* переменных (см. .env.example),
    подключаясь к localhost.
    """
    url = os.getenv("DATABASE_URL")
    if url:
        return url

    user = os.getenv("POSTGRES_USER", "user")
    password = os.getenv("POSTGRES_PASSWORD", "user")
    db = os.getenv("POSTGRES_DB", "ttt_db")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")

    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{db}"
