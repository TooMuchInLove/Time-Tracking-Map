from psycopg2.errors import (SyntaxError, NoDataFound, UniqueViolation, NumericValueOutOfRange,
                             CheckViolation, ProgrammingError, OperationalError)


class PostgresNumericValueOutOfRangeError(NumericValueOutOfRange):
    """ Ошибка числового значения при запросе к Базе Данных PostgreSQL. """
    error = "[POSTGRES_NUMERIC_VALUE_ERROR] Числовое значение выходит за пределы допустимого диапазона."


class PostgresUniqueViolationError(UniqueViolation):
    """ Ошибка нарушения уникальности значений при запросе к Базе Данных PostgreSQL. """
    error = "[POSTGRES_UNIQUE_VIOLATION_ERROR] Ошибка нарушения уникальности значений при запросе."


class PostgresCheckViolationError(CheckViolation):
    """ Ошибка нарушения проверки значения при запросе к Базе Данных PostgreSQL. """
    error = "[POSTGRES_CHECK_VIOLATION_ERROR] Ошибка нарушения проверки значения при запросе."


class PostgresProgrammingError(ProgrammingError):
    """ Ошибка выполнения не корректного запроса к Базе Данных PostgreSQL. """
    error = "[POSTGRES_PROGRAMMING_ERROR] Не удаётся выполнить запрос. Запрос пустой или с ошибкой."


class PostgresConnectionError(OperationalError):
    """ Ошибка подключения к Базе Данных PostgreSQL. """
    error = "[POSTGRES_CONNECTION_ERROR] Подключение к '%s:%s/%s' прервано!"


class PostgresInvalidRequestError(SyntaxError):
    """ Ошибка выполнения запроса к Базе Данных PostgreSQL. """
    error = "[POSTGRES_INVALID_REQUEST_ERROR] Из-за ошибки синтаксиса выполнение запроса отклонено."


class PostgresNoDataFoundError(NoDataFound):
    """ Ошибка отсутствия данных к Базе Данных PostgreSQL. """
    error = "[POSTGRES_NO_DATA_FOUND_ERROR] По самосвалу нет последней информации для обновления."
