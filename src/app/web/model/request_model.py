from pydantic import BaseModel, Field, field_validator
from uuid import UUID
from typing import List

class BoardRequest(BaseModel):
    grid: List[List[int]] = Field(
        ...,
        min_length=3,
        max_length=3,
        description="3x3 игровое поле: 0 - пусто, 1 - X (человек), -1 - O (компьютер)"
    )

    @field_validator('grid')
    def check_grid_dimensions(cls, v):
        if len(v) != 3:
            raise ValueError('grid must have exactly 3 rows')
        for row in v:
            if len(row) != 3:
                raise ValueError('each row must have exactly 3 columns')
            for cell in row:
                if cell not in (-1, 0, 1):
                    raise ValueError('cell value must be -1, 0, or 1')
        return v

class GameRequest(BaseModel):
    id: UUID = Field(..., alias="id")  # JSON может приходить с ключом "id"
    board: BoardRequest
