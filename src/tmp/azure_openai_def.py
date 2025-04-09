import requests
from requests import Response
import os


# 0) 사용자 개인 thread 생성
def _create_new_thread(azure_openai_endpoint, azure_openai_api_key):
    PERSONAL_THREAD_ENDPOINT = f'https://{azure_openai_endpoint}/openai/threads?api-version=2024-05-01-preview'

    result = requests.post(
        PERSONAL_THREAD_ENDPOINT,
        headers={
            'api-key': azure_openai_api_key,
            'Content-Type': 'application/json'
        }
    )

    PERSONAL_THREAD_ID = result.json()['id']
    return PERSONAL_THREAD_ID


# 1) thread에 신규 질문 발송
def _add_user_question_to_thread(azure_openai_endpoint, azure_openai_api_key, personal_thread_id, user_question) -> Response:
    USER_QUESTION_ENDPOINT = f'https://{azure_openai_endpoint}/openai/threads/{personal_thread_id}/messages?api-version=2024-05-01-preview'

    result = requests.post(
        USER_QUESTION_ENDPOINT,
        headers={
            'api-key': azure_openai_api_key,
            'Content-Type': 'application/json'
        },
        json={
            'role': 'user',
            'content': user_question
        }
    )
    return result


# 2-1) thread 실행
def _run_thread(azure_openai_endpoint, azure_openai_api_key, personal_thread_id, assistant_id):
    USER_QUESTION_RUN_ENDPOINT = f'https://{azure_openai_endpoint}/openai/threads/{personal_thread_id}/runs?api-version=2024-05-01-preview'

    result = requests.post(
        USER_QUESTION_RUN_ENDPOINT,
        headers={
            'api-key': azure_openai_api_key,
            'Content-Type': 'application/json'
        },
        json={
            'assistant_id': assistant_id
        }
    )
    if result.status_code != 200:
        return

    RUN_ID = result.json()['id']
    return RUN_ID


# 2-2) thread 모니터링 및 응답 대기
def _get_status_of_run(azure_openai_endpoint, azure_openai_api_key, personal_thread_id, run_id):
    TEMP_RUN_ENDPOINT = f'https://{azure_openai_endpoint}/openai/threads/{personal_thread_id}/runs/{run_id}?api-version=2024-05-01-preview'

    result = requests.get(
        TEMP_RUN_ENDPOINT,
        headers={
            'api-key': azure_openai_api_key,
        }
    )

    return result.json()['status']


# 3) 응답 수신 및 출력 # 마지막 text value로 가져오기
def _get_assistant_response(azure_openai_endpoint, azure_openai_api_key, personal_thread_id):
    USER_QUESTION_ENDPOINT = f'https://{azure_openai_endpoint}/openai/threads/{personal_thread_id}/messages?api-version=2024-05-01-preview'

    result = requests.get(
        USER_QUESTION_ENDPOINT,
        headers={
            'api-key': azure_openai_api_key,
            'Content-Type': 'application/json'
        }
    )
    if result.status_code != 200:
        return

    response = result.json()
    messages = response['data']

    # 가장 최근 assistant 메시지 찾기
    for message in messages:
        if message['role'] == 'assistant':
            return message['content'][0]['text']['value']


def send_message_to_thread(thread_id: str, assistant_id: str, message: str) -> any:
    ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
    API_KEY = os.getenv('AZURE_OPENAI_API_KEY')

    result = _add_user_question_to_thread(
        ENDPOINT, API_KEY, thread_id, message)
    if result.status_code != 200:
        return

    run_id = _run_thread(ENDPOINT, API_KEY, thread_id, assistant_id)
    return run_id


def is_run_done(thread_id: str, run_id: str) -> bool:
    return 'completed' == _get_status_of_run(os.getenv('AZURE_OPENAI_ENDPOINT'),
                                             os.getenv('AZURE_OPENAI_API_KEY'),
                                             thread_id, run_id)


def get_last_assistant_message(thread_id: str) -> str | None:
    return _get_assistant_response(os.getenv('AZURE_OPENAI_ENDPOINT'),
                                   os.getenv('AZURE_OPENAI_API_KEY'),
                                   thread_id)
