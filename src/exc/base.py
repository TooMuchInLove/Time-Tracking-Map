class ReceivingHeaderDataError(IndexError):
    """ Ошибка при получении данных заголовка """
    error = "[RECEIVING_HEADER_DATA_ERROR] Ошибка при получении данных заголовка!"


class ReceivingMessageDataError(KeyError):
    """ Ошибка при получении данных сообщения """
    error = "[RECEIVING_MESSAGE_DATA_ERROR] Ошибка при получении ключевых данных из сообщения!"
