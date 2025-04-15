import json

from src.logic.app_logic import app_logic
from src.ui.messages import convert_to_openai_style
from src.ui.constants import ASSISTANTS_OF_MODE, Modes


def queue_message(content, chat_state):
    if content.strip():
        message = {'role': 'user', 'content': content}
        chat_state['histories'][chat_state['mode']].append(message)
        chat_state['histories'][chat_state['mode']].append(
            {'role': 'assistant', 'content': '허리 피세요'})
    return chat_state['histories'][chat_state['mode']], chat_state


def wait_message(content, chat_state):
    mode = chat_state['mode']
    if not content.strip():
        return '', chat_state['histories'][mode], chat_state

    # GENERAL 모드일 때만 처리
    if mode == Modes.GENERAL:
        # GENERAL 모드의 기본 응답 처리
        response = app_logic.get_response_from_assistant(
            ASSISTANTS_OF_MODE[mode],
            content
        )
        # 첫 번째 메시지 추가
        main_message = convert_to_openai_style(response)
        chat_state['histories'][mode].append(main_message)

        # main_message의 content에서 코드 블록 제거
        raw_content = main_message['content'].strip()
        if raw_content.startswith("```") and raw_content.endswith("```"):
            raw_content = raw_content[raw_content.find(
                '\n') + 1:raw_content.rfind('\n')].strip()

        # JSON 변환 시도
        try:
            message_json = json.loads(raw_content)
        except json.JSONDecodeError:
            # JSON 변환 실패 시 에러 메시지 추가
            error_message = {
                'role': 'assistant',
                'content': "⚠️ 응답 메시지를 처리하는 중 오류가 발생했습니다. 올바른 형식의 JSON이 아닙니다."
            }
            chat_state['histories'][mode].append(error_message)
            return '', chat_state['histories'][mode], chat_state

        # JSON 응답에서 true인 항목에 대해 추가 처리
        if message_json.get("job", False):
            additional_response = app_logic.get_response_from_assistant(
                ASSISTANTS_OF_MODE[Modes.JOB],
                content
            )
            additional_message = convert_to_openai_style(
                additional_response)
            app_logic.add_dialogue_thread(
                role="assistant", message=additional_message['content'])
            chat_state['histories'][mode].append(additional_message)

        if message_json.get("resume", False):
            additional_response = app_logic.get_response_from_assistant(
                ASSISTANTS_OF_MODE[Modes.RESUME],
                content
            )
            additional_message = convert_to_openai_style(
                additional_response)
            app_logic.add_dialogue_thread(
                role="assistant", message=additional_message['content'])
            chat_state['histories'][mode].append(additional_message)

        if message_json.get("roadmap", False):
            additional_response = app_logic.get_response_from_assistant(
                ASSISTANTS_OF_MODE[Modes.ROADMAP],
                content
            )
            additional_message = convert_to_openai_style(
                additional_response)
            app_logic.add_dialogue_thread(
                role="assistant", message=additional_message['content'])
            chat_state['histories'][mode].append(additional_message)

        if message_json.get("recruitment", False):
            additional_response = app_logic.get_response_from_assistant(
                ASSISTANTS_OF_MODE[Modes.RECRUIT],
                content
            )
            additional_message = convert_to_openai_style(
                additional_response)
            app_logic.add_dialogue_thread(
                role="assistant", message=additional_message['content'])
            chat_state['histories'][mode].append(additional_message)

    else:
        # GENERAL이 아닌 경우 기본 응답 처리
        response = app_logic.get_response_from_assistant(
            ASSISTANTS_OF_MODE[mode],
            content
        )
        message = convert_to_openai_style(response)
        chat_state['histories'][mode].pop()
        chat_state['histories'][mode].append(message)

    return '', chat_state['histories'][chat_state['mode']], chat_state
