
import logging
import os
from pathlib import Path
import sys
import tomllib
import structlog


class MediationLogConfig:

    # singleton pattern to ensure only one instance of MediationConfig exists
    def __new__(cls, *args, **kwargs):
        cls.__create_instance()
        return cls.instance

    @classmethod
    def __create_instance(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MediationLogConfig, cls).__new__(cls)

    @classmethod
    def getInstance(cls):
        cls.__create_instance()
        return cls.instance

    # this exists only so that testing framework can reinitialize the singleton config with test parameters
    def reconfigure(self, root=None):
        self._initialized=False
        self.__init_once__(root)

    def __init__(self, root=None):
        self.__init_once__(root)

    def __init_once__(self, root=None):
        # singleton initialization check
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.root = Path(root or ".")
        config_path=str(self.root / "pyproject.toml")

        with open(config_path, "rb") as f:
            self._config = tomllib.load(f)
            self._logconfig=self._config.get("tool",{}).get("mediation_logs", {}).get("logconfig", {})
            self._logsdir = self.root / self._logconfig.get("logsdir", "logs")
            os.makedirs(self._logsdir, exist_ok=True) 
        self.setup_logging()
        self._initialized = True

    def loggername(self):
        return self._logconfig.get("loggername", "mediation")
    
    def logfile_txt(self):
        return self._logsdir / self._logconfig.get("logfile", "mediation_logs.log")
    
    def logfile_json(self):
        return self._logsdir / self._logconfig.get("jsonfile", "mediation_logs.json")

    def setup_logging(self):
        processor_formatter = structlog.stdlib.ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(),  # Or KeyValueRenderer for plain text
        foreign_pre_chain=[
            pass_destination,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.add_log_level,
            structlog.processors.format_exc_info
        ])

        setup_structlog()
        logger = logging.getLogger(self.loggername())
        logger.addHandler(make_handler("console",logging.StreamHandler(sys.stdout),processor_formatter))
        logger.addHandler(make_handler("file",logging.FileHandler(self.logfile_txt(), mode='a'),processor_formatter))
        logger.addHandler(make_handler("json_file",logging.FileHandler(self.logfile_json(), mode='a'),processor_formatter))

    def get_logger(self, destination=None):
        logger = structlog.get_logger(self.loggername())
        return logger.bind(destination=destination) if destination else logger

def pass_destination(logger, method_name, event_dict):
    record = event_dict.get("_record")
    if record is not None and "destination" in event_dict:
        record.destination = event_dict["destination"]
    return event_dict

def setup_structlog():
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter 
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
