import threading
from uuid import UUID
from typing import Dict, Any, Optional

class GameStorage:
    def __init__(self) -> None:
        self._data: Dict[UUID, Any] = {}
        self._lock = threading.Lock()

    def put(self, key: UUID, value: Any) -> None:
        with self._lock:
            self._data[key] = value

    def get(self, key: UUID) -> Optional[Any]:
        with self._lock:
            return self._data.get(key)
