from contextlib import asynccontextmanager
from fastapi import FastAPI

from tic_tac_toe.web.route.game_route import router
from tic_tac_toe.di.container import Container
from tic_tac_toe.infrastructure.database.base import Base
from tic_tac_toe.infrastructure.database.session import engine
# Импорт модели нужен, чтобы она зарегистрировалась в Base.metadata до create_all.
from tic_tac_toe.infrastructure.persistence.model.game_model import GameModel  # noqa: F401


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создаём таблицы при старте, если их ещё нет.
    # Для учебного проекта этого достаточно; в реальном проекте здесь были бы
    # Alembic-миграции вместо create_all.
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield


def create_app() -> FastAPI:
    app = FastAPI(
        title="Tic-Tac-Toe API",
        description="REST API для игры в крестики-нолики с алгоритмом Минимакс.",
        version="2.0.0",
        docs_url="/docs",        # Интерактивная документация Swagger
        redoc_url="/redoc",       # Альтернативная документация ReDoc
        lifespan=lifespan,
    )
    # Создаём DI-контейнер и сохраняем в состоянии приложения
    container = Container()
    app.state.container = container
    # Подключаем роутер с эндпоинтами
    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
