import tomllib
import json
import importlib.resources

class MediationConfig:

    # singleton pattern to ensure only one instance of MediationConfig exists
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MediationConfig, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self._config = tomllib.load(open("pyproject.toml", "rb"))
        self._logconfig=self._config.get("tool",{}).get("mediation_logs", {}).get("logconfig", {})
        self._jsonconfig=self._config.get("tool",{}).get("mediation_logs", {}).get("jsonconfig", {})
        self._data= self._load_json()
    
    def _load_json(self):
        json_file_path = importlib.resources.files("data").joinpath(self._jsonconfig.get("jsondata"))
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
        json.load()
    
