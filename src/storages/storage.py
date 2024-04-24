from dataclasses import dataclass


@dataclass(slots=True)
class StatesOfMachine:
    """ Хранилище для некоторых состояний машины. """
    is_with_cargo: bool = None  # Машина с/без грузом/а [True/False]
    is_active: bool = None  # Активность/Не активность экскаватора
    is_idle: bool = None  # Простой машины
    last_mes_time: str = None  # Время последнего события
    last_uuid: str = None  # Последний уникальный идентификатор сообщения
    last_uuid_unload: str = None  # Последний уникальный идентификатор сообщения для разгрузки
    stopping_id: int = None  # Код причины остановки техники (машины)
    mileage: str = "null"  # Обычный пробег
    gps_mileage: str = "null"  # GPS пробег
    fuel_consumption: str = "null"  # Топливо
    engine_hours: str = "null"  # Моточасы
    coordinates: str = "null"  # Координаты машины по x, y, z


@dataclass(slots=True, frozen=True)
class MainFields:
    """ Общие поля у всех типов сообщений. """
    object_id: int  # ID машины
    uuid: str  # Уникальный ID текущего сообщения
    mes_time: str  # Время начала события
    mileage: str  # Обычный пробег
    gps_mileage: str  # GPS пробег
    fuel_consumption: str  # Топливо
    engine_hours: str  # Моточасы
    coordinates: str  # Координаты машины по x, y, z


@dataclass(slots=True, frozen=True)
class OtherFields(MainFields):
    """ Другие нетипичные поля. """
    stopping_id: int  # Код причины остановки машины
