# main.py
from fastapi import FastAPI
from app.web.route.game_route import router
from app.di.container import Container

def create_app() -> FastAPI:
    app = FastAPI(
        title="Tic-Tac-Toe API",
        description="REST API для игры в крестики-нолики с алгоритмом Минимакс.",
        version="1.0.0",
        docs_url="/docs",        # Интерактивная документация Swagger
        redoc_url="/redoc"       # Альтернативная документация ReDoc
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
