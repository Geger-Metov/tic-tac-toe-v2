from pydantic import BaseModel, Field
from uuid import UUID
from typing import List

class BoardResponse(BaseModel):
    grid: List[List[int]]

class GameResponse(BaseModel):
    game_id: UUID = Field(..., alias="id")  # В JSON будет поле "id"
    board: BoardResponse

    model_config = {
        "validate_by_name": True,   # аналог allow_population_by_field_name
        "populate_by_name": True    # разрешает передавать "game_id" при создании объекта
    }
