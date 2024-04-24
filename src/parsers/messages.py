from json import loads as json_loads
from storages import MainFields, OtherFields
from exc import ReceivingHeaderDataError, ReceivingMessageDataError
from config import EventType as ET


def parse_header(header: dict) -> str:
    """ Парсинг заголовка сообщения для определения события.
    :param header: заголовок или значение события
    :return: событие """
    command = list(header)
    if not command:
        raise ReceivingHeaderDataError
    return command[0]


def parse_message(body: bytes, command: str) -> MainFields | OtherFields:
    """ Разбиваем сообщения по соответствующим структурам.
    :param body: сообщение байтов от брокера
    :param command: заголовок или значение события
    :return: структура, хранящая некоторые ключевые параметры """
    message: dict = dict(json_loads(body.decode()))  # Преобразовываем сообщение байтов в словарь
    main_data: dict = message.get("data")
    event_data: dict = message.get("event_data")
    object_id: int = message.get("object_id")
    if main_data is None or event_data is None or object_id is None:
        raise ReceivingMessageDataError
    if command in (ET.STOP, ET.START, ET.ACTIVITY, ET.NOT_ACTIVITY, ET.LOAD, ET.UNLOAD):
        return OtherFields(
            object_id=object_id,
            uuid=_get_uuid(main_data),
            mes_time=_get_mes_time(message),
            stopping_id=_get_stopping_id(event_data),
            mileage=_get_mileage(main_data),
            gps_mileage=_get_mileage(main_data, is_gps=True),
            fuel_consumption=_get_fuel_consumption(main_data),
            engine_hours=_get_engine_hours(main_data),
            coordinates=_get_coordinates(main_data),
        )
    elif command == ET.REGULAR:
        return MainFields(
            object_id=object_id,
            uuid=_get_uuid(main_data),
            mes_time=_get_mes_time(message),
            mileage=_get_mileage(main_data),
            gps_mileage=_get_mileage(main_data, is_gps=True),
            fuel_consumption=_get_fuel_consumption(main_data),
            engine_hours=_get_engine_hours(main_data),
            coordinates=_get_coordinates(main_data),
        )


def _get_uuid(data: dict) -> str:
    return _wrap_string_value_in_quote(data.get("_id"))


def _get_mes_time(data: dict) -> str:
    return _wrap_string_value_in_quote(data.get("mes_time"))


def _get_stopping_id(data: dict) -> int:
    return _conversion_numeric_value(data.get("reason"))


def _get_mileage(data: dict, is_gps: bool = False) -> str:
    if is_gps:
        return _conversion_string_value(data.get("gps_mileage"))
    return _conversion_string_value(data.get("mileage"))


def _get_fuel_consumption(data: dict) -> str:
    return _conversion_string_value(data.get("fuel_consumption"))


def _get_engine_hours(data: dict) -> str:
    return _conversion_string_value(data.get("engine_hours"))


def _get_coordinates(data: dict) -> str:
    return _conversion_coordinates(data.get('x'), data.get('y'), data.get('z'))


def _wrap_string_value_in_quote(value: str) -> str:
    """ Обернуть строковое значение в кавычки. """
    return "null" if value is None else f"'{value}'"


def _conversion_string_value(value: str) -> str:
    """ Преобразование строковых значений. """
    return "null" if value is None else f"{value}"


def _conversion_numeric_value(value: str) -> int | None:
    """ Преобразование строковых значений в числовые. """
    return None if value is None else int(value)


def _conversion_coordinates(x: float, y: float, z: float) -> str:
    """ Разбираем координаты и приводим их к строке для записи в БД. """
    return f"jsonb_build_object('x', {'null' if x is None else x}, " \
           f"'y', {'null' if y is None else y}, 'z', {'null' if z is None else z})"
