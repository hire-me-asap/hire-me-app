import requests
import os
from openai import AzureOpenAI
from openai.types import VectorStore


AZURE_OPENAI_CLIENT: AzureOpenAI = AzureOpenAI(
    api_key=os.getenv('AZURE_OPENAI_API_KEY'),
    api_version="2024-05-01-preview",
    azure_endpoint=f'https://{os.getenv('AZURE_OPENAI_ENDPOINT')}/'
)


def azure_openai_request(header: dict, body: dict) -> any:
    """기본 요청 함수"""
    
    pass


def request_something1_to_openai(*args, **kwargs) -> any:
    """특정 요청 함수"""
    
    header = None
    body = None
    
    azure_openai_request(header=header, body=body)


def get_vector_store(name: str) -> VectorStore:
    """이름으로 기존 벡터 스토어를 찾아 반환합니다. 존재하지 않는 이름이라면 새 벡터 스토어를 생성해 반환합니다.

    Args:
        name (str): 필요한 벡터 스토어의 이름

    Returns:
        VectorStore: 해당 이름을 가진 벡터 스토어
    """
    for vs in AZURE_OPENAI_CLIENT.vector_stores.list():
        if vs.name == name:
            vector_store = vs
            break
    else:
        vector_store = AZURE_OPENAI_CLIENT.vector_stores.create(name=name)
    return vector_store