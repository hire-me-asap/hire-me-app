import json
import re

from typing import Tuple
from src.logic.app_logic import app_logic
from src.logic.app_logic import app_logic


RESUME_SEPARATOR = '\n---resume start---\n'
RESUME_IN_USER_MESSAGE = '\n---\n📜 *질문에 이력서가 포함되어있습니다.*'
RESUME_IN_ASSISTANT_MESSAGE = '\n---\n📝 *답변에 이력서가 포함되어있습니다.*'


def convert_to_openai_style(raw_json_message: dict) -> dict:
    """
    raw JSON 메시지를 OpenAI 스타일로 변환합니다.

    매개변수:
        raw_json_message (dict): 변환할 raw JSON 메시지.

    반환값:
        dict: OpenAI 스타일로 변환된 메시지.
    """
    # 원본 텍스트 가져오기
    raw_content = raw_json_message['content'][0]['text']['value']
    # 정규표현식으로 【...】 형식 제거
    cleaned_content = re.sub(r'【.*?】', '', raw_content)

    message = {
        'role': raw_json_message['role'],
        'content': cleaned_content
    }

    if RESUME_SEPARATOR in message['content']:
        if message['role'] == 'user':
            message['content'] = message['content'].split(
                RESUME_SEPARATOR)[0] + RESUME_IN_USER_MESSAGE
        else:
            message['content'] = message['content'].split(
                RESUME_SEPARATOR)[0] + RESUME_IN_ASSISTANT_MESSAGE

  message['raw_message'] = raw_json_message
   return message


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

    if "---json start---" in content:
        # 텍스트와 이미지 분리
        try:
            message = convert_to_openai_style(raw_json_message)
            message_id = message['raw_message']['id']
            message_text, roadmap_image = app_logic.split_roadmap_text_image(
                message['content'], message_id)
        except ValueError:  # json start 구분자가 없거나 파싱 실패 시
            message_text = message['content']
            roadmap_image = None

        # 이미지 URL 생성 및 텍스트에 추가
        if roadmap_image:
            message_image = f"/gradio_api/file=static/roadmap/{roadmap_image.split('/')[-1]}"
            message_text += f"\n---\n<img src='{message_image}' alt='Roadmap Image'/>"

        # 메시지 업데이트
        message['content'] = message_text

    if "---json start---" in content:
        # 텍스트와 이미지 분리
        try:
            message = convert_to_openai_style(raw_json_message)
            message_id = message['raw_message']['id']
            message_text, roadmap_image = app_logic.split_roadmap_text_image(
                message['content'], message_id)
        except ValueError:  # json start 구분자가 없거나 파싱 실패 시
            message_text = message['content']
            roadmap_image = None

        # 이미지 URL 생성 및 텍스트에 추가
        if roadmap_image:
            message_image = f"/gradio_api/file=static/roadmap/{roadmap_image.split('/')[-1]}"
            message_text += f"\n---\n<img src='{message_image}' alt='Roadmap Image'/>"

        # 메시지 업데이트
        message['content'] = message_text

    return message, {}


def convert_roadmap_to_openai_style(raw_json_message: dict) -> dict:
    """
    raw_json_message 중에서 mode가 roadmap일 경우 텍스트와 이미지를 분할한 뒤,
    텍스트에 이미지 URL을 포함한 HTML 형식으로 변환하여 반환합니다.

    Args:
        raw_json_message (dict): 변환할 raw JSON 메시지.

    Returns:
        dict: OpenAI 스타일로 변환된 메시지.
    """
    # OpenAI 스타일 기본 변환
    message = convert_to_openai_style(raw_json_message)
    message_id = message['raw_message']['id']

    # role이 assistant인 경우에만 이미지 분리 수행
    if message['role'] == 'assistant':
        # 텍스트와 이미지 분리
        try:
            message_text, roadmap_image = app_logic.split_roadmap_text_image(
                message['content'], message_id)
        except ValueError:  # json start 구분자가 없거나 파싱 실패 시
            message_text = message['content']
            roadmap_image = None

        # 이미지 URL 생성 및 텍스트에 추가
        if roadmap_image:
            message_image = f"/gradio_api/file=static/roadmap/{roadmap_image.split('/')[-1]}"
            message_text += f"\n---\n<img src='{message_image}' alt='Roadmap Image'/>"

        # 메시지 업데이트
        message['content'] = message_text

    return message



def convert_roadmap_to_openai_style(raw_json_message: dict) -> dict:
    """
    raw_json_message 중에서 mode가 roadmap일 경우 텍스트와 이미지를 분할한 뒤,
    텍스트에 이미지 URL을 포함한 HTML 형식으로 변환하여 반환합니다.

    Args:
        raw_json_message (dict): 변환할 raw JSON 메시지.

    Returns:
        dict: OpenAI 스타일로 변환된 메시지.
    """
    # OpenAI 스타일 기본 변환
    message = convert_to_openai_style(raw_json_message)
    message_id = message['raw_message']['id']

    # role이 assistant인 경우에만 이미지 분리 수행
    if message['role'] == 'assistant':
        # 텍스트와 이미지 분리
        try:
            message_text, roadmap_image = app_logic.split_roadmap_text_image(
                message['content'], message_id)
        except ValueError:  # json start 구분자가 없거나 파싱 실패 시
            message_text = message['content']
            roadmap_image = None

        # 이미지 URL 생성 및 텍스트에 추가
        if roadmap_image:
            message_image = f"/gradio_api/file=static/roadmap/{roadmap_image.split('/')[-1]}"
            message_text += f"\n---\n<img src='{message_image}' alt='Roadmap Image'/>"

        # 메시지 업데이트
        message['content'] = message_text

    return message
