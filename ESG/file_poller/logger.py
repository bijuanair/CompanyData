# file_poller/logger.py

import logging
from .config import LOG_LEVEL


def setup_logger():
    logger = logging.getLogger("file_poller")
    logger.setLevel(LOG_LEVEL)

    if not logger.handlers:
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger