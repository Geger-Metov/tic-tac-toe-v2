from app.domain.model.game import Game as DomainGame
from app.domain.model.board import Board as DomainBoard
from app.web.model.request_model import GameRequest
from app.web.model.response_model import GameResponse, BoardResponse

class GameWebMapper:
    @staticmethod
    def request_to_domain(request: GameRequest) -> DomainGame:
        return DomainGame(
            id=request.id,
            board=DomainBoard(grid=request.board.grid)
        )

    @staticmethod
    def domain_to_response(domain: DomainGame) -> GameResponse:
        return GameResponse(
            id=domain.id,
            board=BoardResponse(grid=domain.board.grid)
        )
