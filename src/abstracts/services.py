from typing import Callable
from abc import ABC, abstractmethod


class AStorage(ABC):
    """ Интерфейс всех хранилищ (SQL, NoSQL). """
    __slots__ = ()

    @abstractmethod
    def connect(self) -> None:
        pass


class AStorageSQL(AStorage):
    """ Интерфейс для всех SQL-хранилищ. """
    __slots__ = ()

    @abstractmethod
    def udi(self, query: str) -> None:
        pass

    @abstractmethod
    def get(self, query: str) -> tuple:
        pass


class AStorageNoSQL(AStorage):
    """ Интерфейс для всех NoSQL-хранилищ. """
    __slots__ = ()

    @abstractmethod
    def read(self, callback: Callable) -> None:
        pass

    @abstractmethod
    def start(self) -> None:
        pass
