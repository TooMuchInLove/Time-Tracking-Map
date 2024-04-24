from sys import stdout as sys_stdout
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class EventType:
    """ Список событий, необходимых для обработки данных, полученных с RabbitMQ. """
    REGULAR = "DB_MSG_TYPE_REGULAR"
    STOP = "DB_MSG_TYPE_STOP"
    START = "DB_MSG_TYPE_START"
    LOAD = "DB_MSG_TYPE_LOAD"
    UNLOAD = "DB_MSG_TYPE_UNLOAD"
    ACTIVITY = "DB_MSG_TYPE_ACTIVITY"
    NOT_ACTIVITY = "DB_MSG_TYPE_NOT_ACTIVITY"
    CODE_LOADING = 253  # Погрузка
    CODE_UNLOADING = 254  # Разгрузка


@dataclass(slots=True, frozen=True)
class SystemStatus:
    """ Список системных статусов. """
    UNLOADING = "DB_CYCLE_CODE_UNLOADING"  # Разгрузка
    STOPPING_EMPTY = "DB_CYCLE_CODE_STOPPING_EMPTY"  # Стоянка/остановка без груза
    MOVEMENT_EMPTY = "DB_CYCLE_CODE_MOVEMENT_EMPTY"  # Движение без груза
    LOADING = "DB_CYCLE_CODE_LOADING"  # Погрузка
    STOPPING_LOAD = "DB_CYCLE_CODE_STOPPING_LOAD"  # Стоянка/остановка с грузом
    MOVEMENT_LOAD = "DB_CYCLE_CODE_MOVEMENT_LOAD"  # Движение с грузом


@dataclass(slots=True, frozen=True)
class Success:
    """ Сообщения об успешных действиях в системе. """
    POSTGRES_CONNECTION = "[POSTGRES_CONNECTION] Подключение к '%s:%s/%s' выполнено успешно!"
    POSTGRES_DISCONNECTION = "[POSTGRES_DISCONNECTION] Соединение закрыто."
    RABBIT_CONNECTION = "[RABBIT_CONNECTION] Подключение к '%s:%s/%s' выполнено успешно!"
    RABBIT_DISCONNECTION = "[RABBIT_DISCONNECTION] Соединение закрыто."
    RABBIT_SETUP = "[RABBIT_SETUP] Настройки выполнены успешно!"


# Конфигурация для loguru
log_config = {
    "handlers": [
        {
            "sink": sys_stdout,
            "colorize": True,
            "level": "DEBUG",
            "backtrace": True,
            "diagnose": True
        },
    ]
}
