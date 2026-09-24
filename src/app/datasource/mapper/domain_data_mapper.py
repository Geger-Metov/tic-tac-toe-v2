from app.domain.model.game import Game as DomainGame
from app.domain.model.board import Board as DomainBoard
from app.datasource.model.game_dts import DataGame, DataBoard

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
