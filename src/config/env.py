from os import environ as os_environ
from dataclasses import dataclass
from .base import EventType as ET


@dataclass(slots=True, frozen=True)
class EnvPostgresDB:
    # Данные для подключения к БД Postgres.
    HOST = os_environ.get("ASD_POSTGRES_HOST")
    PORT = os_environ.get("ASD_POSTGRES_PORT")
    DB_NAME = os_environ.get("ASD_POSTGRES_DBNAME")
    USER_NAME = os_environ.get("SERVICE_PG_TTM_USERNAME")
    PASSWORD = os_environ.get("SERVICE_PG_TTM_PASSWORD")
    # URL для подключения к БД Postgres.
    URL = f"postgresql://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"
    # Время, через которое будет осуществлено переподключение
    CONNECT_TIMEOUT = int(os_environ.get("SERVICE_PG_CONNECT_TIMEOUT", 10))


@dataclass(slots=True, frozen=True)
class EnvRabbitMQ:
    # Данные для подключения к RabbitMQ.
    HOST = os_environ.get("ASD_RMQ_HOST")
    VHOST = os_environ.get("ASD_RMQ_VHOST")
    PORT = os_environ.get("ASD_RMQ_PORT")
    HEARTBEAT = os_environ.get("ASD_RMQ_HEARTBEAT")
    USER_NAME = os_environ.get("SERVICE_RMQ_ILOGIC_USERNAME")
    PASSWORD = os_environ.get("SERVICE_RMQ_ILOGIC_PASSWORD")
    # URL для подключения к RabbitMQ.
    URL = f"amqp://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{VHOST}?heartbeat={HEARTBEAT}"
    # Название очереди и обмен событиями
    NAME_QUEUE = os_environ.get("SERVICE_RMQ_QUEUE")
    EXCHANGE = os_environ.get("SERVICE_RMQ_EXCHANGE")
    PREFETCH_COUNT = 1  # Кол-во предварительных выборок
    # Время, через которое будет осуществлено переподключение
    CONNECT_TIMEOUT = int(os_environ.get("SERVICE_RMQ_CONNECT_TIMEOUT", 10))

    @staticmethod
    def get_bind() -> dict:
        return {
            "x-match": "any",
            ET.REGULAR: True,
            ET.STOP: True,
            ET.START: True,
            ET.LOAD: True,
            ET.UNLOAD: True,
            ET.ACTIVITY: True,
            ET.NOT_ACTIVITY: True,
        }


env_postgres = EnvPostgresDB()

env_rabbit = EnvRabbitMQ()
