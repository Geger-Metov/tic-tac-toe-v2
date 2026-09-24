from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.model.game import Game

class IGameService(ABC):
    @abstractmethod
    def get_next_move(self, game: Game) -> Game:
        pass

    @abstractmethod
    def validate_field(self, old_game: Game, new_game: Game) -> bool:
        pass

    @abstractmethod
    def is_game_over(self, game: Game) -> bool:
        pass

    @abstractmethod
    def process_user_move_and_computer_response(self, user_game: Game) -> Game:
        pass

    @abstractmethod
    def get_game_by_id(self, id: UUID) -> Game:
        pass

    @abstractmethod
    def save_game(self, game: Game) -> None:
        pass
