# tic-tac-toe-v2

Tic-Tac-Toe REST API: FastAPI + SQLAlchemy (async) + PostgreSQL, с алгоритмом Minimax
для хода компьютера. Управление зависимостями и окружением — через [uv](https://docs.astral.sh/uv/).

## Локальный запуск (без Docker)

```bash
uv sync                     # создаст .venv и поставит зависимости из uv.lock
cp .env.example .env        # и поправь значения под себя
uv run uvicorn tic_tac_toe.main:app --reload --app-dir src
```

## Запуск в Docker

```bash
cp .env.example .env
docker compose up --build
# или, для разработки с live-reload при изменении src/:
docker compose watch
```

## Добавление зависимости

```bash
uv add <package>            # обновит pyproject.toml и uv.lock
```
