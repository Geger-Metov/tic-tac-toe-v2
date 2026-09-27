from tic_tac_toe.domain.model.game import Game as DomainGame
from tic_tac_toe.domain.model.board import Board as DomainBoard
from tic_tac_toe.infrastructure.persistence.model.game_model import GameModel


def to_data(domain: DomainGame) -> GameModel:
    return GameModel(
        id = domain.id,
        board = domain.board.grid
    )


def to_domain(data: GameModel) -> DomainGame:
    return DomainGame(
        id = data.id,
        board = DomainBoard(grid=data.board)
    )
