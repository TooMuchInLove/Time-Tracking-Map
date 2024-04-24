from loguru import logger
from time import perf_counter
from pika.spec import Basic, BasicProperties
from pika.channel import Channel
from parsers import parse_message, parse_header
from storages import (PostgresDB, RabbitMQ, StatesOfMachine, insert_machine, insert_record,
                      update_record, update_penultimate_record, get_latest_record, OtherFields,
                      get_record_of_last_loading_or_unloading, update_system_status)
from exc import ReceivingHeaderDataError, ReceivingMessageDataError
from config import EventType as ET, SystemStatus as SS, env_postgres as env_pg, env_rabbit as env_rmq


class Facade:
    """ Выполняет работу по взаимодействию между БД и брокером сообщений. """
    __slots__ = ("__db", "__mq", "__machines",)

    def __init__(self) -> None:
        self.__db = PostgresDB(env_pg.URL)
        self.__mq = RabbitMQ(env_rmq.URL)
        self.__machines = {}

    def start(self) -> None:
        """ Начало работы с сообщениями, получаемые от хранилища. """
        self.__mq.read(self.__callback)
        self.__mq.start()

    def __callback(self, channel: Channel, method: Basic.Deliver, properties: BasicProperties, body: bytes) -> None:
        """ Метод для получения сообщений из брокера.
        :param channel: канал связи
        :param method: метод доставки
        :param properties: свойства сообщения
        :param body: тело сообщения """
        try:
            tic = perf_counter()
            command = parse_header(properties.headers)
            msg = parse_message(body, command)
            if msg is None:
                return None
            logger.info(f"[{msg.object_id}] [{command}] uuid={msg.uuid}, time={msg.mes_time}")
            state_of_machine = self.get_state_of_machine(msg.object_id, msg.mes_time)

            if command == ET.STOP:
                if state_of_machine.is_idle is not None and not state_of_machine.is_idle:
                    update_record(self.__db, state_of_machine.last_uuid, state_of_machine.last_mes_time)
                system_status = set_system_status(state_of_machine.is_idle, msg, state_of_machine.is_with_cargo)
                update_penultimate_record(self.__db, msg, state_of_machine, system_status)
                insert_record(self.__db, msg, command, msg.stopping_id)
                state_of_machine = save_state_of_machine(state_of_machine, msg, True)

            elif command == ET.START:
                if state_of_machine.is_idle:
                    update_record(self.__db, state_of_machine.last_uuid, state_of_machine.last_mes_time)
                system_status = set_system_status(state_of_machine.is_idle, msg, state_of_machine.is_with_cargo)
                update_penultimate_record(self.__db, msg, state_of_machine, system_status)
                insert_record(self.__db, msg, command)
                state_of_machine = save_state_of_machine(state_of_machine, msg, False)

            elif command == ET.ACTIVITY:
                if state_of_machine.is_active is not None and not state_of_machine.is_active:
                    update_record(self.__db, state_of_machine.last_uuid, state_of_machine.last_mes_time)
                update_penultimate_record(self.__db, msg, state_of_machine, ET.NOT_ACTIVITY)
                insert_record(self.__db, msg, command)
                state_of_machine.last_uuid = msg.uuid
                state_of_machine.is_active = True

            elif command == ET.NOT_ACTIVITY:
                if state_of_machine.is_active:
                    update_record(self.__db, state_of_machine.last_uuid, state_of_machine.last_mes_time)
                update_penultimate_record(self.__db, msg, state_of_machine, ET.ACTIVITY)
                insert_record(self.__db, msg, command)
                state_of_machine.last_uuid = msg.uuid
                state_of_machine.is_active = False

            elif command == ET.REGULAR:
                state_of_machine.last_mes_time = msg.mes_time
                state_of_machine.mileage = msg.mileage
                state_of_machine.gps_mileage = msg.gps_mileage
                state_of_machine.fuel_consumption = msg.fuel_consumption
                state_of_machine.engine_hours = msg.engine_hours
                state_of_machine.coordinates = msg.coordinates

            elif command == ET.LOAD:
                update_record(self.__db, state_of_machine.last_uuid, state_of_machine.last_mes_time)
                state_of_machine.is_with_cargo = True

            elif command == ET.UNLOAD:
                update_record(self.__db, state_of_machine.last_uuid_unload, stopping_id=msg.stopping_id)
                if not state_of_machine.is_idle:
                    system_status = set_system_status(True, msg)
                    update_system_status(self.__db, state_of_machine.last_uuid_unload, system_status)
                state_of_machine.is_with_cargo = False

            self.__machines[msg.object_id] = state_of_machine
            logger.debug(f"ОБЩЕЕ ВРЕМЯ РАБОТЫ С СООБЩЕНИЕМ: {perf_counter()-tic:.4f} сек.")
        except IndexError:
            logger.error(ReceivingHeaderDataError.error)
        except KeyError:
            logger.error(ReceivingMessageDataError.error)
        finally:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    def get_state_of_machine(self, object_id: int, mes_time: str) -> StatesOfMachine:
        """ Получение актуальных данных (при каждом запуске сервиса). """
        state = self.__machines.get(object_id)
        if state is None:
            insert_machine(self.__db, object_id)
            state = create_state_of_machine(
                get_latest_record(self.__db, object_id),
                get_record_of_last_loading_or_unloading(self.__db, object_id), mes_time)

        return state


def create_state_of_machine(data1: tuple[str, int, bytes], data2: tuple[int], mes_time: str) -> StatesOfMachine:
    """ Создание начального состояния параметров одной единицы техники (машины). """
    state = StatesOfMachine()

    command, stopping_id, uuid = (None, None, None,) if data1 is None else data1
    state.stopping_id = stopping_id
    state.last_uuid = "null" if uuid is None else f"'{str(uuid, 'utf-8')}'"
    state.last_uuid_unload = "null"
    state.last_mes_time = mes_time

    if command == ET.STOP:
        state.is_idle = True
    elif command == ET.START:
        state.is_idle = False
    else:
        state.is_idle = None

    stopping_id = None if data2 is None else data2[0]
    state.is_with_cargo = False
    if stopping_id == ET.CODE_LOADING:
        state.is_with_cargo = True

    return state


def save_state_of_machine(state: StatesOfMachine, message: OtherFields, is_idle: bool) -> StatesOfMachine:
    """ Сохранение состояния параметров 1 единицы техники (машины). """
    state.last_uuid = message.uuid
    if is_idle:
        state.last_uuid_unload = message.uuid
    state.stopping_id = message.stopping_id
    state.is_idle = is_idle

    return state


def set_system_status(is_idle: bool, message: OtherFields, is_with_cargo: bool = None) -> str | None:
    """ Определяем и устанавливаем системный статус. """
    if is_idle:
        if message.stopping_id == ET.CODE_LOADING:
            return SS.LOADING
        elif message.stopping_id == ET.CODE_UNLOADING:
            return SS.UNLOADING
        elif is_with_cargo:
            return SS.STOPPING_LOAD
        elif not is_with_cargo:
            return SS.STOPPING_EMPTY
        return None
    if is_with_cargo:
        return SS.MOVEMENT_LOAD
    elif not is_with_cargo:
        return SS.MOVEMENT_EMPTY
    return None
