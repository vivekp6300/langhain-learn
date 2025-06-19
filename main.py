import os
from dotenv import load_dotenv
from langchain_community.chat_models import ChatOpenAI
import logging_setup

OPENAI_KEY_NAME="OPENAI_API_KEY"
load_dotenv()


def main():
    logger = logging_setup.Logger()
    logger.console_log.info(f"OpenAI Key = {os.getenv(OPENAI_KEY_NAME)}")

if (__name__=="__main__"):
    main()