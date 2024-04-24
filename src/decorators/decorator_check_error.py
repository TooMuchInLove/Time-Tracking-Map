from loguru import logger
from typing import Callable
from exc import (SyntaxError, NoDataFound, UniqueViolation, CheckViolation,
                 ProgrammingError, NumericValueOutOfRange, PostgresNumericValueOutOfRangeError,
                 PostgresInvalidRequestError, PostgresNoDataFoundError, PostgresProgrammingError,
                 PostgresCheckViolationError, PostgresUniqueViolationError,)


def is_check_error(function: Callable) -> Callable:
    """ Декоратор для проверки объекта подключения на ошибки. """
    def _wrapper(self, *args, **kwargs) -> None:
        try:
            return function(self, *args, **kwargs)
        except NumericValueOutOfRange:
            logger.error(PostgresNumericValueOutOfRangeError.error)
        except UniqueViolation:
            logger.error(PostgresUniqueViolationError.error)
        except CheckViolation:
            logger.error(PostgresCheckViolationError.error)
        except SyntaxError:
            logger.error(PostgresInvalidRequestError.error)
        except ProgrammingError:
            logger.error(PostgresProgrammingError.error)
        except NoDataFound:
            logger.error(PostgresNoDataFoundError.error)
    return _wrapper
