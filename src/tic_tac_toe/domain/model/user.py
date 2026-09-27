from dataclasses import dataclass
from uuid import UUID

@dataclass
class User:
    id: UUID
    login: str
    passwd_hash: str
