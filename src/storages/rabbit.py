from loguru import logger
from typing import Callable
from pika import BlockingConnection, URLParameters
from socket import gaierror
from decorators import is_check_connect
from abstracts import AStorageNoSQL
from mixins import MixinConnection, MixinReconnection, MixinChannel
from exc import (ProbableAuthenticationError, ProbableAccessDeniedError, AMQPConnectionError, ChannelClosedByBroker,
                 RabbitChannelClosedByBroker, ChannelWrongStateError, RabbitChannelWrongStateError,
                 RabbitProbableAuthenticationError, RabbitProbableAccessDeniedError, RabbitConnectionError,)
from config import Success, env_rabbit as env_rmq


class RabbitMQ(AStorageNoSQL, MixinConnection, MixinChannel, MixinReconnection):
    """ Хранилище. Брокер сообщений RabbitMQ. """
    __slots__ = ("__url", "connection", "channel",)

    def __init__(self, url: str) -> None:
        """ Инициализация атрибутов.
        :param url: адрес для подключения """
        MixinConnection.__init__(self)
        MixinChannel.__init__(self)
        self.__url = url
        self.connect()
        MixinReconnection.reconnect(self)

    def connect(self) -> None:
        """ Подключение к брокеру сообщений. """
        try:
            self.connection = BlockingConnection(URLParameters(self.__url))
            self.channel = self.connection.channel()
            logger.success(Success.RABBIT_CONNECTION % (env_rmq.HOST, env_rmq.PORT, env_rmq.VHOST))
            self.__setup()
        except (ProbableAuthenticationError, ValueError):
            logger.error(RabbitProbableAuthenticationError.error)
        except (AMQPConnectionError, gaierror):
            logger.error(RabbitConnectionError.error)
        except ProbableAccessDeniedError:
            logger.error(RabbitProbableAccessDeniedError.error)

    @is_check_connect(is_channel=True)
    def __setup(self) -> None:
        """ Объявление и настройка очереди. Установка некоторых параметров для работы. """
        self.channel.queue_declare(queue=env_rmq.NAME_QUEUE, durable=True, exclusive=False, auto_delete=False)
        self.channel.queue_bind(queue=env_rmq.NAME_QUEUE, exchange=env_rmq.EXCHANGE, arguments=env_rmq.get_bind())
        self.channel.basic_qos(prefetch_count=env_rmq.PREFETCH_COUNT)
        logger.success(Success.RABBIT_SETUP)

    @is_check_connect(is_channel=True)
    def read(self, callback: Callable) -> None:
        """ Настройка канала связи для чтения пакетов сообщений. """
        try:
            self.channel.basic_consume(queue=env_rmq.NAME_QUEUE, auto_ack=False, on_message_callback=callback)
        except ChannelClosedByBroker:
            logger.error(RabbitChannelClosedByBroker.error)

    @is_check_connect(is_channel=True)
    def start(self) -> None:
        """ Старт: получаем сообщения. """
        try:
            self.channel.start_consuming()
        except ChannelWrongStateError:
            logger.error(RabbitChannelWrongStateError.error)
        except KeyboardInterrupt:
            self.channel.stop_consuming()

    def __del__(self) -> None:
        """ Разрываем соединение с брокером сообщений. """
        if MixinConnection.is_connect(self):
            self.connection.close()
            logger.success(Success.RABBIT_DISCONNECTION)
