from fastapi import APIRouter, Depends, HTTPException, status, Request
from uuid import UUID

from app.web.model.request_model import GameRequest
from app.web.model.response_model import GameResponse
from app.web.mapper.domain_web_mapper import GameWebMapper
from app.domain.service.game_interface import IGameService
from app.domain.model.game import Game
from app.domain.model.board import Board

router = APIRouter(prefix="/game", tags=["game"])

def get_game_service(request: Request) -> IGameService:
    """Извлекает сервис из DI-контейнера, сохранённого в app.state."""
    container = request.app.state.container
    return container.get_game_service()

@router.post("/{game_id}", response_model=GameResponse)
async def make_move(
    id: UUID,
    request_data: GameRequest,
    service: IGameService = Depends(get_game_service)
):
    # 1. Проверка совпадения UUID
    if request_data.id != id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game ID in URL and body must match"
        )

    # 2. Преобразуем запрос в доменную модель
    incoming_game = GameWebMapper.request_to_domain(request_data)

    # 3. Загружаем или создаём новую игру
    try:
        current_game = service.get_game_by_id(id)
    except ValueError:
        # Игра не найдена — создаём новую с пустым полем
        current_game = Game(id=id, board=Board.create_empty())
        # Сохраняем её в репозитории (можно через сервис, если добавить метод)
        service.save_game(current_game)  # или service.save_game(current_game)

    # 4. Валидация хода пользователя
    if not service.validate_field(current_game, incoming_game):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid move: you can only change one empty cell to X"
        )

    # 5. Сохраняем ход пользователя
    service.save_game(incoming_game)  # или service.save_game(incoming_game)

    # 6. Если игра не окончена, получаем ход компьютера
    if not service.is_game_over(incoming_game):
        updated_game = service.get_next_move(incoming_game)
    else:
        updated_game = incoming_game

    # 7. Возвращаем ответ
    return GameWebMapper.domain_to_response(updated_game)
