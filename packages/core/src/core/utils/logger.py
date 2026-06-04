import logging
import sys
from typing import List

from core.base_storage import BaseStorage
from core.version import __version__ as core_version


class StreamRedirector:
    def __init__(self, logger, log_level):
        self.logger = logger
        self.log_level = log_level
        self._is_logging = False

    def write(self, message):
        if message.strip() and not self._is_logging:
            self._is_logging = True
            try:
                self.logger.log(self.log_level, message.strip())
            finally:
                self._is_logging = False

    def flush(self):
        pass


def setup_logging():
    storage = BaseStorage("AstraLauncher")
    log_dir = storage.get_path("logs")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "latest.log"

    handlers: List[logging.Handler] = [
        logging.FileHandler(log_file, encoding="utf-8", mode="w")
    ]

    if sys.__stdout__ is not None:
        handlers.append(logging.StreamHandler(sys.__stdout__))

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(message)s",
        datefmt="%H:%M:%S",
        handlers=handlers,
    )

    logging.raiseExceptions = False

    sys.stdout = StreamRedirector(logging.getLogger("STDOUT"), logging.INFO)
    sys.stderr = StreamRedirector(logging.getLogger("STDERR"), logging.ERROR)

    def exception_handler(exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        logging.error(
            "Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback)
        )

    sys.excepthook = exception_handler
    logging.info(f"Core Version: {core_version}")
