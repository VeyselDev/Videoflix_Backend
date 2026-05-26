import logging
from typing import Any
import os


"""
Centralized logging utility.

Configures a module-level logger based on the environment and provides
simple wrapper functions for consistent logging usage across the project.
"""

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
    """Logs a debug-level message."""
    logger.debug(message, *args, **kwargs)


def log_info(message: str, *args: Any, **kwargs: Any) -> None:
    """Logs an info-level message."""
    logger.info(message, *args, **kwargs)


def log_warning(message: str, *args: Any, **kwargs: Any) -> None:
    """Logs a warning-level message."""
    logger.warning(message, *args, **kwargs)


def log_error(message: str, *args: Any, **kwargs: Any) -> None:
    """Logs an error-level message."""
    logger.error(message, *args, **kwargs)


def log_exception(message: str, *args: Any, **kwargs: Any) -> None:
    """
    Logs an exception with stack trace information.

    Should be used inside except blocks.
    """
    logger.exception(message, *args, **kwargs)