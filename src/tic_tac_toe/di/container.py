from sqlalchemy.ext.asyncio import AsyncSession

from tic_tac_toe.datasource.repository.game_repository import GameRepo
from tic_tac_toe.datasource.service.game_service_impl import GameService
from tic_tac_toe.domain.service.game_interface import IGameService

class Container:
    """
    DI-контейнер.

    GameStorage больше не нужен: данные теперь хранятся в PostgreSQL, доступ к
    которой даёт SQLAlchemy AsyncSession. Session привязана к жизненному циклу
    одного HTTP-запроса (см. infrastructure.database.session.get_db_session),
    поэтому GameRepo/GameService здесь принципиально НЕ синглтоны — они
    создаются заново на каждый запрос, с той самой request-scoped session.
    """

    def get_game_service(self, session: AsyncSession) -> IGameService:
        repo = GameRepo(session)
        return GameService(repo)
