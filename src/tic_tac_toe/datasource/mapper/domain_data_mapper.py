from tic_tac_toe.domain.model.game import Game as DomainGame
from tic_tac_toe.domain.model.board import Board as DomainBoard
from tic_tac_toe.datasource.model.game_dts import DataGame, DataBoard

def to_data(domain: DomainGame) -> DataGame:
    return DataGame(
        id = domain.id,
        board = DataBoard(grid = domain.board.grid)
    )

def to_domain(data: DataGame) -> DomainGame:
    return DomainGame(
        id = data.id,
        board = DomainBoard(grid=data.board.grid)
    )
