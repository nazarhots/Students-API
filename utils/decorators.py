import time

from sqlalchemy.exc import SQLAlchemyError, OperationalError

from config import MAX_DB_RETRIES, RETRIES_SLEEP_INTERVAL
from logger.logger import create_logger


logger = create_logger()
error_msg = "An unexpected error has occurred, and our team is currently investigating the issue."


def retry_db_operation(func):
    def wrapper(*args, **kwargs):
        for attempt in range(MAX_DB_RETRIES):
            try:
                return func(*args, **kwargs)
            except (SQLAlchemyError, OperationalError):
                logger.debug(
                    f"Lost connection with DB, sleep {RETRIES_SLEEP_INTERVAL} sec and will retry (attempt {attempt})"
                )
                time.sleep(RETRIES_SLEEP_INTERVAL)
                if attempt == MAX_DB_RETRIES - 1:
                    raise 
            except Exception:
                raise
    return wrapper


def retry_app_db_operation(func):
    def wrapper(*args, **kwargs):
        for attempt in range(MAX_DB_RETRIES):
            try:
                return func(*args, **kwargs)
            except OperationalError:
                logger.debug(
                    f"Lost connection with DB, sleep {RETRIES_SLEEP_INTERVAL} sec and will retry (attempt {attempt})"
                )
                time.sleep(RETRIES_SLEEP_INTERVAL)
                continue
            except Exception as error:
                logger.error(str(error))
                return error_msg, 500
        logger.error("No connection to database")
        return error_msg, 500
    return wrapper
