import json
from typing import Tuple


def convert_to_openai_style(raw_json_message: dict) -> dict:
    """
    raw JSON 메시지를 OpenAI 스타일로 변환합니다.

    매개변수:
        raw_json_message (dict): 변환할 raw JSON 메시지.

    반환값:
        dict: OpenAI 스타일로 변환된 메시지.
    """
    return {
        'role': raw_json_message['role'], 
        'content': raw_json_message['content'][0]['text']['value']
    }

def convert_general_response_to_openai_style(raw_json_message: dict) -> Tuple[dict, dict]:
    """무물 스레드의 메시지를 OpenAI 스타일로 변환하고, 메시지를 json으로 해석해서 dict로 변환한 객체와 함께 반환합니다.

    Args:
        raw_json_message (dict): 변환할 raw JSON 메시지.

    Returns:
        tuple[dict, dict]: 변환된 메시지와 JSON 객체
    """
    message = convert_to_openai_style(raw_json_message)
    content = message['content'].strip()
    
    if content.startswith('```json\n'):
        try:
            message_json = json.loads(content.strip('`')[5::])
        except json.JSONDecodeError:
            error_message = {
                'role': 'assistant',
                'content': "⚠️ 죄송합니다. 알 수 없는 오류가 발생했습니다. 잠시 후에 다시 메시지를 전송해주세요."
            }
            return error_message, {}

        message['content'] = message_json['message']
        return message, message_json

    return message, {}