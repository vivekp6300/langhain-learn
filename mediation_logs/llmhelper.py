import json
from dotenv import load_dotenv, find_dotenv
import tomllib
import logging


from jinja2 import Template
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.tools import Tool
from mediation_logs.util.log_handler import MediationLogConfig
from mediation_logs.util.json_handler import MediationJSONConfig

OPENAI_KEY_NAME="OPENAI_API_KEY"
CONFIG_PROMPTS = "prompts"
CONFIG_STOCK_PROMPT = "test_stock_entry"

_ = load_dotenv(find_dotenv())

jsonconfig = MediationJSONConfig.getInstance()
logconfig = MediationLogConfig.getInstance()

tools = [
    Tool.from_function(func=jsonconfig.add_or_overwrite_log,name="add_log_entry",description="Add a log entry with period and details."),
    Tool.from_function(func=jsonconfig.merge_log,name="update_mediation_logs",description="Update the mediation logs for a given period with new details."),
    Tool.from_function(func=jsonconfig.get_log, name="get_log_entry", description="Get the log entry for a given period."),
    Tool.from_function(func=jsonconfig.get_all_logs, name="get_all_log_entries", description="Get all the log entries")
    ]

def get_intent(user_message):
    # log = logconfig.get_logger("console") is not working at the moment
    log = logging.getLogger("llmhelper")
    intent_prompt = MediationJSONConfig.getInstance().intent_prompt.render({"user_input":user_message})
    llm = ChatOpenAI()
    response = llm.invoke(intent_prompt)
    log.info(f"LLM Response: {response}")
    content = response.content
    if isinstance(content, str):
        intent_json = json.loads(content)
    else:
        raise ValueError(f"Expected string in response.content, got {type(content)}: {content}")
    return intent_json

def handle(user_message):
    intent_json = get_intent(user_message)
    intent = intent_json.get("intent", "NONE")
    details = intent_json.get("details", "")
    period = intent_json.get("period","NONE")
    if (intent == "add"):
        return jsonconfig.add_or_overwrite_log(period, details)
    return "Currently I don't know how to do that"