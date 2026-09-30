# tic-tac-toe-v2

Tic-Tac-Toe REST API: FastAPI + SQLAlchemy (async) + PostgreSQL, с алгоритмом Minimax
для хода компьютера. Управление зависимостями и окружением — через [uv](https://docs.astral.sh/uv/).

## Локальный запуск (без Docker)

```bash
uv sync                     # создаст .venv и поставит зависимости из uv.lock
cp .env.example .env        # и поправь значения под себя (нужна доступная PostgreSQL)
uv run alembic upgrade head # применить миграции — без этого таблиц в БД не будет
uv run uvicorn tic_tac_toe.main:app --reload --app-dir src
```

## Запуск в Docker

```bash
cp .env.example .env
docker compose up --build
# или, для разработки с live-reload при изменении src/ или migrations/:
docker compose watch
```

Миграции применяются автоматически при старте контейнера `app`
(см. `docker-entrypoint.sh`) — руками ничего гонять не нужно.

## Миграции базы данных (Alembic)

Схему БД версионирует Alembic (`migrations/`), а не `Base.metadata.create_all()`.

```bash
# применить все ещё не применённые миграции
uv run alembic upgrade head

# откатить последнюю миграцию
uv run alembic downgrade -1

# после того как поменял SQLAlchemy-модель — сгенерировать новую миграцию
# (нужна доступная БД, alembic сравнивает модели с реальной схемой)
uv run alembic revision --autogenerate -m "описание изменения"
# всегда проверяй сгенерированный файл в migrations/versions/ перед коммитом —
# autogenerate не идеален (например, не всегда видит переименования колонок)

# посмотреть текущую версию БД / полную историю
uv run alembic current
uv run alembic history
```

## Тесты

```bash
uv sync                     # dev-группа (pytest/httpx) ставится по умолчанию
uv run alembic upgrade head # тестам нужна уже смигрированная БД
uv run pytest               # юнит + интеграционные (последние бьют по реальной БД,
                             # но каждый тест откатывается — мусора не остаётся)

uv run pytest tests/unit    # только быстрые тесты бизнес-логики, БД не нужна
uv run pytest -v -k login   # конкретный сценарий
```

Интеграционные тесты (`tests/integration/`) дёргают приложение в процессе через
ASGI (без поднятого `uvicorn`/`/docs`), но пишут в ту БД, что указана в
`DATABASE_URL` — проще всего гонять их с поднятым `docker compose up` (порт
БД проброшен на хост, см. `POSTGRES_PORT` в `.env`).

## Добавление зависимости

```bash
uv add <package>            # обновит pyproject.toml и uv.lock
```
