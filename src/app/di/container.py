from app.datasource.storage.game_storage import GameStorage
from app.datasource.repository.game_repository import GameRepo
from app.datasource.service.game_service_impl import GameService
from app.domain.service.game_interface import IGameService

class Container:
    """
    DI-контейнер. Создаёт и хранит экземпляры всех зависимостей.
    Обеспечивает singleton-поведение для хранилища и сервисов.
    """
    def __init__(self) -> None:
        # 1. Потокобезопасное хранилище (один экземпляр на всё приложение)
        self._storage = GameStorage()

        # 2. Репозиторий, работающий с хранилищем
        self._repo = GameRepo(self._storage)

        # 3. Сервис бизнес-логики, реализующий интерфейс IGameService
        self._game_service: IGameService = GameService(self._repo)

    def get_game_service(self) -> IGameService:
        """Возвращает готовый к использованию сервис."""
        return self._game_service