from loguru import logger
from psycopg2 import connect as psycopg2_connect
from decorators import is_check_connect, is_check_error
from abstracts import AStorageSQL
from mixins import MixinConnection, MixinReconnection
from exc import PostgresConnectionError, PostgresProgrammingError, OperationalError, ProgrammingError
from config import Success, env_postgres as env_pg


class PostgresDB(AStorageSQL, MixinConnection, MixinReconnection):
    """ Хранилище. База данных PostgreSQL. """
    __slots__ = ("__url", "connection",)

    def __init__(self, url: str) -> None:
        """ Инициализация атрибутов.
        :param url: адрес для подключения """
        MixinConnection.__init__(self)
        self.__url = url
        self.connect()
        MixinReconnection.reconnect(self)

    def connect(self) -> None:
        """ Подключение к базе данных. """
        try:
            self.connection = psycopg2_connect(self.__url)
            self.connection.autocommit = True
            logger.success(Success.POSTGRES_CONNECTION % (env_pg.HOST, env_pg.PORT, env_pg.DB_NAME))
        except OperationalError:
            logger.error(PostgresConnectionError.error)
        except ProgrammingError:
            logger.error(PostgresProgrammingError.error)

    @is_check_connect(is_channel=False)
    @is_check_error
    def udi(self, query: str) -> None:
        """ Отправляем запрос в базу данных (Update, Delete и Insert).
        :param query: строка запроса. """
        with self.connection.cursor() as cursor:
            cursor.execute(query)

    @is_check_connect(is_channel=False)
    @is_check_error
    def get(self, query: str) -> tuple:
        """ Отправляем запрос в базу данных (Get data).
        :param query: строка запроса. """
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            return cursor.fetchone()

    def __del__(self) -> None:
        """ Разрываем соединение с базой данных. """
        if MixinConnection.is_connect(self):
            self.connection.close()
            logger.success(Success.POSTGRES_DISCONNECTION)
