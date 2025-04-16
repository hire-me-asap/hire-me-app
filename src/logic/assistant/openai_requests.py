import requests
from requests import Response
from openai import AzureOpenAI
from openai.types import VectorStore, FileObject

from src.logic.constants import constants

AZURE_OPENAI_CLIENT: AzureOpenAI = AzureOpenAI(
    api_key=constants.AZURE_OPENAI_API_KEY,
    api_version="2024-05-01-preview",
    azure_endpoint=f"https://{constants.AZURE_OPENAI_ENDPOINT}/",
)


def create_new_thread():
    """
    1. 사용자 개인용 Azure OpenAI Thread를 생성합니다.

    Parameters:
        azure_openai_endpoint (str): Azure OpenAI 서비스의 엔드포인트 도메인.
        azure_openai_api_key (str): Azure OpenAI API 인증 키.

    Returns:
        str: 생성된 개인 Thread의 ID.
    """
    PERSONAL_THREAD_ENDPOINT = (
        f"https://{constants.AZURE_OPENAI_ENDPOINT}/openai/threads?api-version=2024-05-01-preview"
    )

    result = requests.post(
        PERSONAL_THREAD_ENDPOINT,
        headers={"api-key": constants.AZURE_OPENAI_API_KEY,
                 "Content-Type": "application/json"},
    )

    PERSONAL_THREAD_ID = result.json()["id"]
    return PERSONAL_THREAD_ID


def delete_thread_id(thread_id: str):
    """
    Azure OpenAI 서비스에서 특정 스레드를 삭제합니다.

    Args:
        thread_id (str): 삭제할 스레드의 ID.

    Raises:
        RuntimeError: 스레드 삭제가 실패한 경우 발생.
    """
    DELETE_THREAD_ENDPOINT = (
        f"https://{constants.AZURE_OPENAI_ENDPOINT}/openai/threads/{thread_id}?api-version=2024-05-01-preview"
    )

    delete_response = requests.delete(
        DELETE_THREAD_ENDPOINT,
        headers={
            "api-key": constants.AZURE_OPENAI_API_KEY,
            "Content-Type": "application/json"
        }
    )

    # 응답 상태 코드 확인
    if delete_response.status_code in [200, 204]:
        print(f"✅ Thread '{thread_id}' has been successfully deleted.")
    else:
        error_message = (
            f"❌ Failed to delete thread '{thread_id}'. "
            f"Status code: {delete_response.status_code}, Response: {delete_response.text}"
        )
        raise RuntimeError(error_message)


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
    USER_QUESTION_ENDPOINT = f"https://{constants.AZURE_OPENAI_ENDPOINT}/openai/threads/{personal_thread_id}/messages?api-version=2024-05-01-preview"

    result = requests.post(
        USER_QUESTION_ENDPOINT,
        headers={"api-key": constants.AZURE_OPENAI_API_KEY,
                 "Content-Type": "application/json"},
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
    USER_QUESTION_RUN_ENDPOINT = f"https://{constants.AZURE_OPENAI_ENDPOINT}/openai/threads/{personal_thread_id}/runs?api-version=2024-05-01-preview"

    result = requests.post(
        USER_QUESTION_RUN_ENDPOINT,
        headers={"api-key": constants.AZURE_OPENAI_API_KEY,
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
    TEMP_RUN_ENDPOINT = f"https://{constants.AZURE_OPENAI_ENDPOINT}/openai/threads/{personal_thread_id}/runs/{run_id}?api-version=2024-05-01-preview"

    result = requests.get(
        TEMP_RUN_ENDPOINT,
        headers={
            "api-key": constants.AZURE_OPENAI_API_KEY,
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


def get_all_assistant_message(personal_thread_id: str) -> str | None:
    """
    4. 특정 Thread에서 최신 Assistant의 응답 메시지를 가져옵니다.

    Parameters:
        personal_thread_id (str): 사용자 개인 Thread의 ID.

    Returns:
        str | None: 가장 최근 Assistant의 텍스트 응답. 없으면 None.
    """
    USER_QUESTION_ENDPOINT = f"https://{constants.AZURE_OPENAI_ENDPOINT}/openai/threads/{personal_thread_id}/messages?api-version=2024-05-01-preview"

    result = requests.get(
        USER_QUESTION_ENDPOINT,
        headers={"api-key": constants.AZURE_OPENAI_API_KEY,
                 "Content-Type": "application/json"},
    )
    if result.status_code != 200:
        return

    response = result.json()
    messages = response["data"]

    return messages


def get_last_assistant_message_one(thread_id: str) -> str | None:
    """
    4.2.2 환경변수에 설정된 엔드포인트를 이용하여 특정 Thread에서 가장 마지막 Assistant 응답 및 annotations를 가져옵니다.

    Parameters:
        thread_id (str): 사용자 개인 Thread의 ID.

    Returns:
        dict | None: 가장 최근 Assistant의 응답. 실패 시 None.
    """
    messages = get_all_assistant_message(thread_id)

    for message in messages:
        if message["role"] == "assistant":
            return message


def get_file_id_name(file_id: str) -> str:
    """파일 아이디를 입력받은 경우, 파일명을 전송"""
    file_info = AZURE_OPENAI_CLIENT.files.retrieve(file_id)
    filename = file_info.filename
    return filename
