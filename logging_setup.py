import logging
import structlog
import sys
import os

def _setup_structlog():
    # --- Structlog Setup ---
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True
    )

def _create_named_logger(name, handler):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False  # KEY: isolate this logger
    return structlog.get_logger(name)

class Logger:

    def __init__(self, 
                 LOG_FILE = "logs/app.log",
                 JSON_FILE = "logs/logpipe.json"):
        """
        Setup logging configuration for the application.
        This includes standard logging and structlog for structured logging.
        """
        os.makedirs("logs", exist_ok=True)  # Ensure the logs directory exists
        _setup_structlog()
        # --- Standard Logging Setup ---
        # Console (human-readable)
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        # File (plain text)
        file_handler = logging.FileHandler(LOG_FILE, mode='a')
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))

        # JSON Pipe/File
        json_file_handler = logging.FileHandler(JSON_FILE, mode='a')  # or use a named pipe
        json_file_handler.setLevel(logging.INFO)
        json_file_handler.setFormatter(logging.Formatter("%(message)s"))

        logging.getLogger("console").addHandler(console_handler)
        logging.getLogger("file").addHandler(file_handler)
        logging.getLogger("json").addHandler(json_file_handler)

        self.console_log = _create_named_logger("console", console_handler)
        self.file_log = _create_named_logger("file", file_handler)
        self.json_log = _create_named_logger("json", json_file_handler)


if (__name__ == "__main__"):
    os.makedirs("tests/logs", exist_ok=True)
    logger = Logger("tests/logs/app.log", "tests/logs/logpipe.json")

    # Example usage
    logger.console_log.info("This is a console log message.")
    logger.file_log.info("This is a file log message.")
    logger.json_log.info("This is a JSON log message.")
    logger.console_log.error("This is an error message with structlog.")

    assert os.path.exists("tests/logs/app.log")
    assert os.path.exists("tests/logs/logpipe.json")
    with open("tests/logs/app.log", "r") as f:
        assert any("This is a file log message." in line for line in f), "File log message missing"

    with open("tests/logs/logpipe.json", "r") as f:
        assert any('"event": "This is a JSON log message."' in line for line in f), "JSON log message missing"
