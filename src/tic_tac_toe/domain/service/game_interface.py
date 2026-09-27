from abc import ABC, abstractmethod
from uuid import UUID

from tic_tac_toe.domain.model.game import Game

class IGameService(ABC):
    # validate_field/is_game_over — чистая логика без обращений к БД, остаются sync.
    @abstractmethod
    def validate_field(self, old_game: Game, new_game: Game) -> bool:
        pass

    @abstractmethod
    def is_game_over(self, game: Game) -> bool:
        pass

    # А эти методы в итоге сохраняют результат в репозиторий (PostgreSQL), поэтому async.
    @abstractmethod
    async def get_next_move(self, game: Game) -> Game:
        pass

    @abstractmethod
    async def process_user_move_and_computer_response(self, user_game: Game) -> Game:
        pass

    @abstractmethod
    async def get_game_by_id(self, id: UUID) -> Game:
        pass

    @abstractmethod
    async def save_game(self, game: Game) -> None:
        pass
