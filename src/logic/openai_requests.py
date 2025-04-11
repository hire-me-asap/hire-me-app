"""
TODO:
- [ ] 벡터 스토어에서 파일 목록을 가져오는 함수 추가
- [ ] 벡터 스토어에 파일 업로드하는 함수 추가
- [ ] 벡터 스토어에서 파일 삭제하는 함수 추가
"""

import os
import requests
from requests import Response
from openai import AzureOpenAI
from openai.types import VectorStore, FileObject


AZURE_OPENAI_CLIENT: AzureOpenAI = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    api_version="2024-05-01-preview",
    azure_endpoint=f"https://{os.getenv('AZURE_OPENAI_ENDPOINT')}/",
)


def get_vector_store(vector_store_name: str) -> str:
    """이름으로 기존 벡터 스토어를 찾아 ID를 반환합니다.
    존재하지 않는 경우, 새로 생성하여 ID를 반환합니다.

    Args:
        vector_store_name (str): 벡터 스토어 이름 (보통 user_id)

    Returns:
        str: 벡터 스토어의 ID
    """
    for vector_store in AZURE_OPENAI_CLIENT.vector_stores.list():
        if vector_store.name == vector_store_name:
            return vector_store.id

    new_vector_store = AZURE_OPENAI_CLIENT.vector_stores.create(name=vector_store_name)
    return new_vector_store.id


def get_vector_store_files_list(vector_store_id: str) -> list[FileObject]:
    """벡터 스토어에서 파일 목록을 가져오는 함수 추가
    Args:
        vector_store_id (str): 벡터 스토어 ID

    Returns:
        list[FileObject]: 벡터 스토어의 파일 목록
    """
    vector_store_files = AZURE_OPENAI_CLIENT.vector_stores.files.list(
        vector_store_id=vector_store_id
    ).data
    file_ids = [file.id for file in vector_store_files]
    files = [AZURE_OPENAI_CLIENT.files.retrieve(file_id) for file_id in file_ids]
    return files


def upload_vector_store_files(vector_store_id: str, files: tuple[str]):
    """벡터 스토어에 파일 업로드하는 함수 추가
    Args:
        vector_store_id (str): 벡터 스토어 ID
        files (tuple[str]): 업로드할 파일 경로가 담긴 튜플
    """
    AZURE_OPENAI_CLIENT.vector_stores.file_batches.create_and_poll(
        vector_store_id=vector_store_id, files=[open(file, mode="rb") for file in files]
    )


def delete_vector_store_files(vector_store_id: str, file_ids: tuple[str]):
    """벡터 스토어에서 파일 삭제

    Args:
        vector_store_id (str): 벡터 스토어 ID
        file_ids (tuple[str]): 삭제할 파일 아이디들이 담긴 튜플
    """
    for file_id in file_ids:
        AZURE_OPENAI_CLIENT.vector_stores.files.delete(
            vector_store_id=vector_store_id, file_id=file_id
        )


# 0) 사용자 개인 thread 생성
def create_new_thread(azure_openai_endpoint, azure_openai_api_key):
    PERSONAL_THREAD_ENDPOINT = (
        f"https://{azure_openai_endpoint}/openai/threads?api-version=2024-05-01-preview"
    )

    result = requests.post(
        PERSONAL_THREAD_ENDPOINT,
        headers={"api-key": azure_openai_api_key, "Content-Type": "application/json"},
    )

    PERSONAL_THREAD_ID = result.json()["id"]
    return PERSONAL_THREAD_ID


# 1) thread에 신규 질문 발송
def add_user_question_to_thread(
    personal_thread_id, user_question
) -> Response:
    ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    USER_QUESTION_ENDPOINT = f"https://{ENDPOINT}/openai/threads/{personal_thread_id}/messages?api-version=2024-05-01-preview"

    result = requests.post(
        USER_QUESTION_ENDPOINT,
        headers={"api-key": API_KEY, "Content-Type": "application/json"},
        json={"role": "user", "content": user_question},
    )
    return result


# 2-1) thread 실행
def _run_thread(
    azure_openai_endpoint, azure_openai_api_key, personal_thread_id, assistant_id
):
    USER_QUESTION_RUN_ENDPOINT = f"https://{azure_openai_endpoint}/openai/threads/{personal_thread_id}/runs?api-version=2024-05-01-preview"

    result = requests.post(
        USER_QUESTION_RUN_ENDPOINT,
        headers={"api-key": azure_openai_api_key, "Content-Type": "application/json"},
        json={"assistant_id": assistant_id},
    )
    if result.status_code != 200:
        return

    RUN_ID = result.json()["id"]
    return RUN_ID

def run_message_to_thread(thread_id: str, assistant_id: str, message: str) -> any:
    ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

    result = _add_user_question_to_thread(ENDPOINT, API_KEY, thread_id, message)
    if result.status_code != 200:
        return

    run_id = _run_thread(ENDPOINT, API_KEY, thread_id, assistant_id)
    return run_id

# 2-2) thread 모니터링 및 응답 대기
def _get_status_of_run(
    azure_openai_endpoint, azure_openai_api_key, personal_thread_id, run_id
):
    TEMP_RUN_ENDPOINT = f"https://{azure_openai_endpoint}/openai/threads/{personal_thread_id}/runs/{run_id}?api-version=2024-05-01-preview"

    result = requests.get(
        TEMP_RUN_ENDPOINT,
        headers={
            "api-key": azure_openai_api_key,
        },
    )

    return result.json()["status"]

def is_run_done(thread_id: str, run_id: str) -> bool:
    return "completed" == _get_status_of_run(
        os.getenv("AZURE_OPENAI_ENDPOINT"),
        os.getenv("AZURE_OPENAI_API_KEY"),
        thread_id,
        run_id,
    )


# 3) 응답 수신 및 출력 # 마지막 text value로 가져오기
def _get_assistant_response(
    azure_openai_endpoint, azure_openai_api_key, personal_thread_id
):
    USER_QUESTION_ENDPOINT = f"https://{azure_openai_endpoint}/openai/threads/{personal_thread_id}/messages?api-version=2024-05-01-preview"

    result = requests.get(
        USER_QUESTION_ENDPOINT,
        headers={"api-key": azure_openai_api_key, "Content-Type": "application/json"},
    )
    if result.status_code != 200:
        return

    response = result.json()
    messages = response["data"]

    # 가장 최근 assistant 메시지 찾기
    for message in messages:
        if message["role"] == "assistant":
            return message["content"][0]["text"]["value"]

def get_last_assistant_message(thread_id: str) -> str | None:
    return _get_assistant_response(
        os.getenv("AZURE_OPENAI_ENDPOINT"), os.getenv("AZURE_OPENAI_API_KEY"), thread_id
    )





