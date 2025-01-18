from logging import getLogger, StreamHandler
from colorlog import ColoredFormatter


class SimpleLogger:
    def __init__(self, log_level: str = "INFO", class_name: str = "app.py"):
        """
        Initialize logger with specified log level.
        """
        self.logger = getLogger(name=class_name)
        self.logger.setLevel(level=log_level.upper())

        # Add handler if it doesn't exist
        if not self.logger.hasHandlers():
            handler = StreamHandler()
            formatter = ColoredFormatter(
                "%(log_color)s%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
                log_colors={
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)

        self.logger.info("Logger initialized")
