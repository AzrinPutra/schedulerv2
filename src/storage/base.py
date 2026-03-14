from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Type, Any

T = TypeVar('T')


class StorageBase(ABC, Generic[T]):
    @abstractmethod
    def save(self, item: T) -> None:
        pass

    @abstractmethod
    def load(self, id: str) -> T:
        pass

    @abstractmethod
    def delete(self, id: str) -> None:
        pass

    @abstractmethod
    def exists(self, id: str) -> bool:
        pass

    @abstractmethod
    def list_all(self) -> list[dict[str, Any]]:
        pass
