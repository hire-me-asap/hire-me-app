import requests

# 0) 사용자 개인 thread 생성
def create_new_thread(azure_openai_endpoint, azure_openai_api_key):
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
def add_user_question_to_thread(azure_openai_endpoint, azure_openai_api_key, personal_thread_id, user_question):
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
    return result.json()


# 2-1) thread 실행
def run_thread(azure_openai_endpoint, azure_openai_api_key, personal_thread_id, assistant_id):
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

    RUN_ID = result.json()['id']
    return RUN_ID


# 2-2) thread 모니터링 및 응답 대기 
def get_status_of_run(azure_openai_endpoint, azure_openai_api_key, personal_thread_id, run_id):
    TEMP_RUN_ENDPOINT = f'https://{azure_openai_endpoint}/openai/threads/{personal_thread_id}/runs/{run_id}?api-version=2024-05-01-preview'

    result = requests.get(
        TEMP_RUN_ENDPOINT, 
        headers={
            'api-key': azure_openai_api_key,
        }
    )

    return result.json()['status']


# 3) 응답 수신 및 출력 # 마지막 text value로 가져오기
def get_assistant_response(azure_openai_endpoint, azure_openai_api_key, personal_thread_id):
    USER_QUESTION_ENDPOINT = f'https://{azure_openai_endpoint}/openai/threads/{personal_thread_id}/messages?api-version=2024-05-01-preview'

    result = requests.get(
        USER_QUESTION_ENDPOINT, 
        headers={
            'api-key': azure_openai_api_key,
            'Content-Type': 'application/json'
        }
    )

    response = result.json()
    messages = response['data']
    
    # 가장 최근 assistant 메시지 찾기
    for message in messages:
        if message['role'] == 'assistant':
            return message['content'][0]['text']['value']
    
    return "응답을 찾을 수 없습니다."