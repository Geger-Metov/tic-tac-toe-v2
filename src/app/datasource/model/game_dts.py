from dataclasses import dataclass
from uuid import UUID

@dataclass
class DataBoard:
    grid: list[list[int]]

@dataclass
class DataGame:
    id: UUID
    board: DataBoard
