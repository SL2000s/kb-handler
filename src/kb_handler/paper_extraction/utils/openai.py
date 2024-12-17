import os

from langchain_openai import AzureChatOpenAI
from langchain.prompts.prompt import PromptTemplate

from ..config.llm_config import (
    GPT4O_API_TYPE,
    GPT4O_API_VERSION,
    GPT4O_AZURE_ENDPOINT_ENV,
    GPT4O_DEPLOYMENT_NAME,
    GPT4O_MODEL_KWARGS,
    GPT4O_MODEL_NAME,
    GPT4O_OPENAI_API_KEY_ENV,
    GPT4O_TEMPERATURE,
)

def _create_client():
    client = AzureChatOpenAI(
        model_name=GPT4O_MODEL_NAME,
        temperature=GPT4O_TEMPERATURE,
        openai_api_type=GPT4O_API_TYPE,
        openai_api_version=GPT4O_API_VERSION,
        deployment_name=GPT4O_DEPLOYMENT_NAME,
        openai_api_key=os.environ.get(GPT4O_OPENAI_API_KEY_ENV, ''),
        azure_endpoint=os.environ.get(GPT4O_AZURE_ENDPOINT_ENV, ''),
        model_kwargs=GPT4O_MODEL_KWARGS,
    )
    return client

def llm_quest(prompt_template: PromptTemplate, **template_variables):
    client = _create_client()
    chain = prompt_template | client
    chain_results = chain.invoke(template_variables)
    result_text = chain_results.content
    return result_text