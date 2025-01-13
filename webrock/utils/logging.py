import logging
import sys
from logging import StreamHandler
from typing import Any


def create_sysout_logging_handler(
    log_level: int = logging.INFO, root_logger: logging.Logger = logging.getLogger()
) -> StreamHandler[Any]:
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(log_level)

    root_logger.addHandler(handler)
    return handler
