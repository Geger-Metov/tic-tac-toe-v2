from uuid import UUID, uuid4

from sqlalchemy.dialects.postgresql.json import JSONB
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from tic_tac_toe.infrastructure.database.base import Base


class GameModel(Base):
    """
    SQLAlchemy-модель игры — она же представление данных на уровне datasource
    (отдельный DTO GameData здесь не заводим: см. ответ на вопрос из TЗ-разбора
    "нужен ли тебе прежний DataGame как DTO" — не нужен, дублировал бы GameModel
    один в один без своей ответственности).
    """
    __tablename__ = "games"

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True, default=uuid4)
    
    # Доска хранится как JSON (List[List[int]]); нормализовывать в отдельную
    # таблицу клеток сейчас избыточно — доска всегда читается/пишется целиком.
    board: Mapped[list] = mapped_column(JSONB, nullable=False)
