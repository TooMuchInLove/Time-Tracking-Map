class MixinChannel:
    """ Проверка канала на закрытие. """
    def __init__(self) -> None:
        self.channel = None

    def is_channel_closed(self) -> bool:
        return self.channel.is_closed
