import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
import structlog

OPENAI_KEY_NAME="OPENAI_API_KEY"
load_dotenv()
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.PrintLoggerFactory,
    wrapper_class=structlog.stdlib.BoundLogger,
)
logger = structlog.get_logger()


def main():
    print(f"OpenAI Key = {os.getenv(OPENAI_KEY_NAME)}")

if (__name__=="__main__"):
    main()