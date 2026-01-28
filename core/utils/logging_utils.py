import logging
from typing import Any
import os


ENV = os.environ.get("ENV", "dev").lower()

logger = logging.getLogger(__name__)


if ENV == "dev":
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)


if not logger.hasHandlers():
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] %(filename)s:%(lineno)d: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def log_debug(message: str, *args: Any, **kwargs: Any) -> None:
    logger.debug(message, *args, **kwargs)

def log_info(message: str, *args: Any, **kwargs: Any) -> None:
    logger.info(message, *args, **kwargs)

def log_warning(message: str, *args: Any, **kwargs: Any) -> None:
    logger.warning(message, *args, **kwargs)

def log_error(message: str, *args: Any, **kwargs: Any) -> None:
    logger.error(message, *args, **kwargs)

def log_exception(message: str, *args: Any, **kwargs: Any) -> None:
    logger.exception(message, *args, **kwargs)