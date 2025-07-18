import logging
import os
import sys
from config.loader import MediationConfig

import structlog

_log_configured = False

def setup_logging():
    os.makedirs("logs", exist_ok=True) 
    setup_structlog()
    config = MediationConfig()
    logger = logging.getLogger(config.loggername())
    if not logger.hasHandlers():
        logger.addHandler(make_handler("console",logging.StreamHandler(sys.stdout)))
        logger.addHandler(make_handler("file",logging.FileHandler(config.logfile_txt(), mode='a')))
        logger.addHandler(make_handler("json_file",logging.FileHandler(config.logfile_json(), mode='a')))


def get_logger(destination=None):
    """
    Returns a preconfigured structlog logger, optionally bound with a destination tag.

    This logger emits structured logs routed to one of several handlers depending on the
    `destination` key. Handlers filter logs by matching the `destination` attached to
    the `LogRecord`.

    If no destination is specified, the logger is returned unbound.

    Args:
        destination (str, optional): The output target to route logs to.
            Must be one of:
            - `"console"` - for stdout logs
            - `"file"` - for plain file output
            - `"json_file"` - for structured JSON logs

    Returns:
        structlog.BoundLogger: A logger ready for structured log emission.

    Raises:
        ValueError: If an invalid destination is provided.

    Example:
        >>> log = get_logger("json_file")
        >>> log.info("user_logged_in", user="vivek")
        # Output goes only to JSON handler
    """
    global _log_configured
    if not _log_configured:
        setup_logging()
        _log_configured = True
    logger = structlog.get_logger(MediationConfig().loggername())
    return logger.bind(destination=destination) if destination else logger

def pass_destination(logger, method_name, event_dict):
    record = event_dict.get('_record',None)
    if (record and 'destination' in event_dict):
        record.destination = event_dict['destination']
    return event_dict

def setup_structlog():
        structlog.configure(
            processors=[
                pass_destination,
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

def make_handler(destination_tag, target, formatter=None, level=logging.INFO):
    handler = target if isinstance(target, logging.Handler) else logging.FileHandler(target, mode='a')
    handler.setLevel(level)
    handler.setFormatter(formatter or logging.Formatter("%(message)s"))
    handler.addFilter(DestinationTagFilter(destination_tag))
    return handler


class DestinationTagFilter(logging.Filter):
    def __init__(self, destination):
        super().__init__()
        self.destination = destination

    def filter(self, record):
        return getattr(record, 'destination', None) == self.destination
