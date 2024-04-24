from pika.exceptions import (ProbableAuthenticationError, ProbableAccessDeniedError,
                             AMQPConnectionError, ChannelClosedByBroker, ChannelWrongStateError)


class RabbitProbableAuthenticationError(ProbableAuthenticationError):
    """ Ошибка аутентификации при попытке подключиться к брокеру сообщений RabbitMQ. """
    error = "[RABBIT_AUTHENTICATION_ERROR] Проблемы при аутентификации. Возможно, неверный логин или пароль."


class RabbitProbableAccessDeniedError(ProbableAccessDeniedError):
    """ Ошибка отказа в доступе при попытке подключиться к брокеру сообщений RabbitMQ. """
    error = "[RABBIT_ACCESS_DENIED_ERROR] Отказ в доступе."


class RabbitConnectionError(AMQPConnectionError):
    """ Ошибка подключения к брокеру сообщений RabbitMQ. """
    error = "[RABBIT_CONNECTION_ERROR] Подключение к '%s:%s/%s' прервано!"


class RabbitChannelClosedByBroker(ChannelClosedByBroker):
    """ Ошибка канала. Канал был закрыт брокером сообщений RabbitMQ. """
    error = "[RABBIT_CHANNEL_CLOSED_ERROR] Канал закрыт брокером."


class RabbitChannelWrongStateError(ChannelWrongStateError):
    """ Ошибка неправильного состояния канала RabbitMQ. """
    error = "[RABBIT_CHANNEL_WRONG_STATE_ERROR] Неправильное состояние канала."
