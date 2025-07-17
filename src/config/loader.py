import tomllib
import json
import importlib.resources
from pathlib import Path

class MediationConfig:

    # singleton pattern to ensure only one instance of MediationConfig exists
    def __new__(cls, *args, **kwargs):
        cls.__create_instance()
        return cls.instance

    @classmethod
    def __create_instance(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MediationConfig, cls).__new__(cls)

    def __init__(self, root=None):
        self.__init_once__(root)

    def __init_once__(self, root=None):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self.root = root or "src"
        config_path=Path(self.root) / "config" / "pyproject.toml"

        with open(config_path, "rb") as f:
            self._config = tomllib.load(f)
            self._logconfig=self._config.get("tool",{}).get("mediation_logs", {}).get("logconfig", {})
            self._jsonconfig=self._config.get("tool",{}).get("mediation_logs", {}).get("jsonconfig", {})
            self._data= self._load_json()
            self._initialized = True

    def reconfigure(self, root=None):
        self._initialized=False
        self.__init_once__(root)

    @classmethod
    def getInstance(cls):
        cls.__create_instance()
        return cls.instance
    
    def _load_json(self):
        json_file_path = Path(self.root) / "data" / self._jsonconfig.get("jsondata")
        with open(json_file_path, "r") as f:
            return json.load(f)

    def loggername(self):
        return self._logconfig.get("loggername", "mediation")
    
    def logsdir(self):
        return self._logconfig.get("logsdir", "logs")
    
    def logfile_txt(self):
        return self._logconfig.get("logfile", "mediation_logs.log")
    
    def logfile_json(self):
        return self._logconfig.get("jsonfile", "mediation_logs.json")
    
    def mediation_logs(self):
        return self._data
    
    def add_log_entry(self, period, details):
        self._data["entries"].append({"period": period, "details": details})

    def get_log(self, period):
        for entry in self._data["entries"]:
            if entry["period"] == period:
                return entry
        return None
    
    def update_log(self, period, details):
        for entry in self._data["entries"]:
            if entry["period"] == period:
                entry["details"] = details
                return True
        return False
