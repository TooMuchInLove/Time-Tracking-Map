from typing import Callable


def is_check_connect(is_channel: bool) -> Callable:
    """ Декоратор для проверки объекта подключения и канала связи на `закрытие`.
    :param is_channel: проверка канала связи
    :return: проверенный объект """
    def _function(function: Callable) -> Callable:
        def _wrapper(self, *args, **kwargs) -> None:
            if self.is_connection_closed():  # Если подключение закрыто, то переподключаемся
                self.reconnect()
            if is_channel:  # Если у объекта есть канал, то:
                if self.is_channel_closed():  # И если канал закрыт, то переподключаемся
                    self.reconnect()
                return function(self, *args, **kwargs)  # Если канал НЕ закрыт!
            return function(self, *args, **kwargs)  # Без проверки канала
        return _wrapper
    return _function
