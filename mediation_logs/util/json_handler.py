import tomllib
import json
from pathlib import Path
import jinja2
from langchain_openai import ChatOpenAI

class MediationJSONConfig:

    # singleton pattern to ensure only one instance of MediationConfig exists
    def __new__(cls, *args, **kwargs):
        cls.__create_instance()
        return cls.instance

    @classmethod
    def __create_instance(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MediationJSONConfig, cls).__new__(cls)

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
        
        # allowing for testing with a different root directory
        self.root = Path(root or ".")
        
        self.setup_prompts()

        config_path=str(self.root / "pyproject.toml")
        
        with open(config_path, "rb") as f:
            
            self._config = tomllib.load(f)
            self.setup_json()
            self._initialized = True

    def setup_json(self):
        self._jsonconfig=self._config.get("tool",{}).get("mediation_logs", {}).get("jsonconfig", {})
        self._json_file_path = Path(self.root) / "resources" / "data" / self._jsonconfig.get("jsondata")
        self._json = self._load_json()
        self._data=  {entry["period"]: entry["details"] for entry in self._json["entries"]}

    def setup_prompts(self):
        jinjaenv=jinja2.Environment(loader=jinja2.FileSystemLoader(searchpath=str(self.root / "resources" / "prompts")))
        self.intent_prompt = jinjaenv.get_template("intent_extractor.j2")
        self.add_prompt = jinjaenv.get_template("add_logs.j2")
        self.merge_prompt = jinjaenv.get_template("merge_logs.j2")
        self.paraphrase_prompt = jinjaenv.get_template("paraphrase_logs.j2")
    
    def _load_json(self):
        with open(self._json_file_path, "r") as f:
            return json.load(f)
        
    def _save_json(self):
        self._json["entries"] = [{"period": period, "details": detail} for period, detail in self._data.items()]    
        with open(self._json_file_path, "w") as f:
            json.dump(self._json, f, indent=4)

    def get_log(self, period):
        if period in self._data:
                return f"Log entry for {period} is {self._data[period]}"
        return f"Log entry not found for period {period}"
    
    def add_or_overwrite_log(self, period, details):
        if period in self._data:
            msg = f"Log entry for period {period} overwritten with new details."
        else:
            msg = f"Log entry for period {period} added with details."
        self._data[period] = details
        return msg
    
    def merge_log(self, period, details):
        if period in self._data:
            self._data[period]=_merge(self._data[period],details)
            return(f"Log entry merged for period {period}")
        else:
            return(f"Nothing there to merge with. Log entry not found for period {period}. Try add_or_overwrite_log instead.")
    
    def get_all_logs(self):
        return self._data
    
    def flush_memory(self):
        self._save_json()
        return "Memory flushed and saved to JSON file."
        
def _merge(original, new):
        llm=ChatOpenAI()
        prompt = MediationJSONConfig.getInstance().merge_prompt.render({"old_details": original, "new_details": new})
        response = llm.invoke(prompt)
        if response is None or not isinstance(response, str):
            raise ValueError("LLM response is not valid. Ensure the LLM is configured correctly.")
        return response.strip()

def _paraphrase(original):
        llm=ChatOpenAI()
        prompt = MediationJSONConfig.getInstance().paraphrase_prompt.render({"details": original})
        response = llm.invoke(prompt)
        if response is None or not isinstance(response, str):
            raise ValueError("LLM response is not valid. Ensure the LLM is configured correctly.")
        return response.strip()
