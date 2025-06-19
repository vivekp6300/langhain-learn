import os
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

OPENAI_KEY_NAME="OPENAI_API_KEY"

load_dotenv()

def main():
    print(f"OpenAI Key = {os.getenv(OPENAI_KEY_NAME)}")

if (__name__=="__main__"):
    main()