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