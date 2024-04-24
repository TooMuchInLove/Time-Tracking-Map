from time import perf_counter
from config import env_postgres as env_pg


class MixinConnection:
    """ Проверка объекта подключения на None и проверка подключения на закрытие. """
    def __init__(self) -> None:
        self.connection = None

    def is_connect(self) -> bool:
        if self.connection is None:
            return False
        return True

    def is_connection_closed(self) -> bool:
        try:
            return self.connection.is_closed
        except AttributeError:
            return self.connection.closed


class MixinReconnection:
    """ Переподключаться к хранилищу, пока подключение не восстановится. """
    def reconnect(self) -> None:
        begin = perf_counter()
        while True:
            if self.is_connect() and not self.is_connection_closed():
                break
            if perf_counter() - begin >= env_pg.CONNECT_TIMEOUT:
                self.connect()
                begin = perf_counter()
