import logging

from config import logger_path


def create_logger():
    logger = logging.getLogger(__name__)
    if logger.hasHandlers():
        return logger

    logger_format = "%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s", "%Y-%m-%d %H:%M:%S"
    path_to_logger = logger_path

    logger.setLevel(logging.INFO)

    file_handler = logging.FileHandler(path_to_logger)
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter(*logger_format)

    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
