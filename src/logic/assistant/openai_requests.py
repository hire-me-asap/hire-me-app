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


def create_new_thread(azure_openai_endpoint, azure_openai_api_key):
    """
    1. 사용자 개인용 Azure OpenAI Thread를 생성합니다.

    Parameters:
        azure_openai_endpoint (str): Azure OpenAI 서비스의 엔드포인트 도메인.
        azure_openai_api_key (str): Azure OpenAI API 인증 키.

    Returns:
        str: 생성된 개인 Thread의 ID.
    """
    PERSONAL_THREAD_ENDPOINT = (
        f"https://{azure_openai_endpoint}/openai/threads?api-version=2024-05-01-preview"
    )

    result = requests.post(
        PERSONAL_THREAD_ENDPOINT,
        headers={"api-key": azure_openai_api_key,
                 "Content-Type": "application/json"},
    )

    PERSONAL_THREAD_ID = result.json()["id"]
    return PERSONAL_THREAD_ID


def add_dialogue_to_thread(
    personal_thread_id, role, message
) -> Response:
    """
    2. 사용자 질문을 지정된 Thread에 추가합니다.

    Parameters:
        personal_thread_id (str): 사용자 개인 Thread의 ID.
        role (str) : 역할(system, user, assistant)
        message (str): thread에 넣을 내용

    Returns:
        Response: 요청 결과에 대한 응답 객체.
    """
    ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    USER_QUESTION_ENDPOINT = f"https://{ENDPOINT}/openai/threads/{personal_thread_id}/messages?api-version=2024-05-01-preview"

    result = requests.post(
        USER_QUESTION_ENDPOINT,
        headers={"api-key": API_KEY, "Content-Type": "application/json"},
        json={"role": role, "content": message},
    )
    return result


def _run_thread(personal_thread_id, assistant_id) -> str:
    """
    3. 지정된 Thread에 대해 Assistant 실행을 트리거합니다.

    Parameters:
        azure_openai_endpoint (str): Azure OpenAI 서비스의 엔드포인트 도메인.
        azure_openai_api_key (str): Azure OpenAI API 인증 키.
        personal_thread_id (str): 사용자 개인 Thread의 ID.
        assistant_id (str): 실행할 Assistant의 ID.

    Returns:
        str | None: 실행된 run의 ID. 실패 시 None 반환.
    """
    ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    USER_QUESTION_RUN_ENDPOINT = f"https://{ENDPOINT}/openai/threads/{personal_thread_id}/runs?api-version=2024-05-01-preview"

    result = requests.post(
        USER_QUESTION_RUN_ENDPOINT,
        headers={"api-key": API_KEY,
                 "Content-Type": "application/json"},
        json={"assistant_id": assistant_id},
    )
    if result.status_code != 200:
        return

    RUN_ID = result.json()["id"]
    return RUN_ID


def run_message_to_thread(thread_id: str, assistant_id: str, role: str, message: str) -> any:
    """
    3.1. 지정된 Thread에 메시지를 추가하고 실행을 시작합니다.

    Parameters:
        thread_id (str): 사용자 개인 Thread의 ID.
        assistant_id (str): 실행할 Assistant의 ID.
        role (str): 역할(system, user, assistant)
        message (str): 사용자 질문 메시지.

    Returns:
        str | None: 실행된 run의 ID. 실패 시 None 반환.
    """

    result = add_dialogue_to_thread(thread_id, role, message)
    if result.status_code != 200:
        return

    run_id = _run_thread(thread_id, assistant_id)
    return run_id


def _get_status_of_run(personal_thread_id, run_id) -> str:
    """
    3.2.1. 실행 중인 run의 상태를 확인합니다.

    Parameters:
        azure_openai_endpoint (str): Azure OpenAI 서비스의 엔드포인트 도메인.
        azure_openai_api_key (str): Azure OpenAI API 인증 키.
        personal_thread_id (str): 사용자 개인 Thread의 ID.
        run_id (str): 실행 중인 run의 ID.

    Returns:
        str: 현재 run의 상태 (예: "queued", "in_progress", "completed" 등).
    """
    ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    TEMP_RUN_ENDPOINT = f"https://{ENDPOINT}/openai/threads/{personal_thread_id}/runs/{run_id}?api-version=2024-05-01-preview"

    result = requests.get(
        TEMP_RUN_ENDPOINT,
        headers={
            "api-key": API_KEY,
        },
    )

    return result.json()["status"]


def is_run_done(thread_id: str, run_id: str) -> bool:
    """
    3.2.2. 주어진 run이 완료되었는지 확인합니다.

    Parameters:
        thread_id (str): 사용자 개인 Thread의 ID.
        run_id (str): 실행 중인 run의 ID.

    Returns:
        bool: run이 완료되었으면 True, 아니면 False.
    """
    return "completed" == _get_status_of_run(
        thread_id,
        run_id,
    )


def _get_assistant_citation(personal_thread_id: str, run_id: str) -> dict | None:
    """
    3.2.3. 주어진 Run ID의 실행 결과 JSON을 반환합니다.

    Parameters:
        personal_thread_id (str): 사용자 고유 Thread ID
        run_id (str): Run ID

    Returns:
        dict | None: Run 결과 JSON (성공 시), None (실패 시)
    """
    ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    RUN_ENDPOINT = f"https://{ENDPOINT}/openai/threads/{personal_thread_id}/runs/{run_id}?api-version=2024-05-01-preview"

    headers = {
        "api-key": API_KEY,
        "Content-Type": "application/json"
    }

    response = requests.get(RUN_ENDPOINT, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(
            f"Failed to get run details: {response.status_code}, {response.text}")
        return None


def get_assistant_citations(thread_id: str, run_id: str) -> dict | None:
    """
    3.2.4. 주어진 Run ID의 실행 결과 JSON을 반환합니다.

    Parameters:
        thread_id (str): 사용자 개인 Thread의 ID.
        run_id: (str) : 실행 중인 Thread의 run ID

    Returns:
        dict | None: Run 결과 JSON (성공 시), None (실패 시)
    """
    return _get_assistant_citation(thread_id, run_id)


def get_all_assistant_response(personal_thread_id: str) -> str | None:
    """
    4. 특정 Thread에서 최신 Assistant의 응답 메시지를 가져옵니다.

    Parameters:
        personal_thread_id (str): 사용자 개인 Thread의 ID.

    Returns:
        str | None: 가장 최근 Assistant의 텍스트 응답. 없으면 None.
    """
    ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
    USER_QUESTION_ENDPOINT = f"https://{ENDPOINT}/openai/threads/{personal_thread_id}/messages?api-version=2024-05-01-preview"

    result = requests.get(
        USER_QUESTION_ENDPOINT,
        headers={"api-key": API_KEY,
                 "Content-Type": "application/json"},
    )
    if result.status_code != 200:
        return

    response = result.json()
    messages = response["data"]

    return messages


def get_last_assistant_message(thread_id: str) -> str | None:
    """
    4.2.2 환경변수에 설정된 엔드포인트를 이용하여 특정 Thread에서 가장 마지막 Assistant 응답을 가져옵니다.

    Parameters:
        thread_id (str): 사용자 개인 Thread의 ID.

    Returns:
        dict | None: 가장 최근 Assistant의 응답. 실패 시 None.
    """
    messages = get_all_assistant_response(thread_id)
    for message in messages:
        if message["role"] == "assistant":
            return message
