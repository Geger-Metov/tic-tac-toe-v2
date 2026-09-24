from uuid import UUID
from typing import Optional

from app.domain.model.game import Game as DomainGame
from app.datasource.mapper.domain_data_mapper import to_data, to_domain
from app.datasource.storage.game_storage import GameStorage

class GameRepo:
    def __init__(self, storage: GameStorage) -> None:
        self._storage = storage
        
    def save(self, game: DomainGame) -> None:
        data_model = to_data(game)
        self._storage.put(game.id, data_model)

    def find_by_id(self, uuid: UUID) -> Optional[DomainGame]:
        data_model = self._storage.get(uuid)
        if data_model is None:
            return None
        
        return to_domain(data_model)
