from dataclasses import dataclass
import uuid

from app.domain.model.board import Board

@dataclass
class Game:
    id: uuid.UUID
    board: Board

    @classmethod
    def create_new_game(cls) -> 'Game':
        return cls(
            id = uuid.uuid4(),
            board = Board.create_empty()
        )
