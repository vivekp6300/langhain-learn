import os
from dotenv import load_dotenv
from logging import logger
import tomllib


from langchain_community.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

OPENAI_KEY_NAME="OPENAI_API_KEY"
CONFIG_PROMPTS = "prompts"
CONFIG_STOCK_PROMPT = "test_stock_entry"

load_dotenv()


def main():
    
    log = logger.getLogger("console")
    openai_key = os.getenv(OPENAI_KEY_NAME)
    config=None
    with (open("pyproject.toml", "rb") as f):
        config=tomllib.load(f)
    log.info(f"OpenAI Key = {openai_key}")

    ''' Old School way :))
    chatgpt = ChatOpenAI(
        openai_api_key=os.getenv(OPENAI_KEY_NAME),
        model_name="gpt-4o",
        temperature=0.0,
        top_p=1,
        frequency_penalty=0.8,
        presence_penalty=0)
    
    logger.info(chatgpt.predict("Do you know the name of the user whose API key you are using?"))
    '''

    # langchain way
    template = config.get(CONFIG_PROMPTS).get(CONFIG_STOCK_PROMPT)

    stock_prompt = PromptTemplate(
        input_variables=["stock_name","time_horizon"],
        template=template
    )

    llm_openai = ChatOpenAI(
        openai_api_key=openai_key, 
        model_name="gpt-4o", 
        model_kwargs={
            "temperature" : 0.0, 
            "top_p" : 1, 
            "frequency_penalty" : 0.8, 
            "presence_penalty": 0}
    )

    llm_chain = LLMChain(llm=llm_openai,prompt=stock_prompt)
    llm_chain_response = llm_chain.run(stock_name="Hyundai",time_horizon="3-5 years")

    logger.info(f"LLM Chain Response: {llm_chain_response}")


if (__name__=="__main__"):
    main()