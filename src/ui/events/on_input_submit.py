import json
import gradio as gr

from src.logic.app_logic import app_logic
from src.ui.messages import convert_to_openai_style, convert_general_response_to_openai_style, RESUME_SEPARATOR, RESUME_IN_USER_MESSAGE
from src.ui.constants import ASSISTANTS_OF_MODE, Modes


PROGRESS_MESSAGE = {'role': 'assistant',
                    'content': '🤧💭 엣취가 답변을 생각하고 있습니다. *허리를 쭉 피세요!!!*',
                    'pop_this': None}


def process_user_message(content, chat_state, resume_state):
    mode = chat_state['mode']
    content = content.strip()
    if not content:
        yield gr.update(), gr.update(), gr.update()
        return

    message = {'role': 'user', 'content': content}

    if chat_state['use_resume']:
        message['content'] += RESUME_IN_USER_MESSAGE
        content += RESUME_SEPARATOR + json.dumps(resume_state, ensure_ascii=False)

    chat_state['histories'][mode].append(message)
    chat_state['histories'][mode].append(PROGRESS_MESSAGE)

    yield '', chat_state['histories'][chat_state['mode']], chat_state

    for _ in _get_assistant_response(content, mode, chat_state, resume_state):
        yield '', chat_state['histories'][chat_state['mode']], chat_state


def _get_assistant_response(content: str, mode: Modes, chat_state, resume_state):
    print(f'@_get_assistant_response({content=}, {mode=}, chat_state)')

    response = app_logic.get_response_from_assistant(
        ASSISTANTS_OF_MODE[mode],
        content
    )
    
    while 'pop_this' in chat_state['histories'][mode][-1]:
        chat_state['histories'][mode].pop()

    if mode not in [Modes.GENERAL, Modes.ROADMAP]:
        message = convert_to_openai_style(response)
        chat_state['histories'][mode].append(message)
        yield message, response
        return

    if mode == Modes.ROADMAP:
        message = convert_to_openai_style(response)
        message_id = message['raw_message']['id']
        message_text, roadmap_image = app_logic.split_roadmap_text_image(
            message['content'], message_id)
        message_image = f"/gradio_api/file=static/roadmap/{roadmap_image.split('/')[-1]}"
        message_text += f"\n---\n<img src='{message_image}' alt='Roadmap Image' width='100%'/>"
        message['content'] = message_text
        chat_state['histories'][mode].append(message)
        yield message, response
        return

    message, json_message = convert_general_response_to_openai_style(response)
    chat_state['histories'][mode].append(message)
    yield

    if not json_message:
        return

    for mode in Modes:
        query = json_message.get(mode.value, '')
        if query:
            message = {'role': 'user', 'content': query}

            if chat_state['use_resume']:
                message['content'] += RESUME_IN_USER_MESSAGE
                query += RESUME_SEPARATOR + json.dumps(resume_state, ensure_ascii=False)

            chat_state['histories'][mode].append(message)
            chat_state['histories'][Modes.GENERAL].append(PROGRESS_MESSAGE)
            yield

            for message, response in _get_assistant_response(query, mode, chat_state, resume_state):
                message['content'] = '\n---\n' + message['content']
                chat_state['histories'][Modes.GENERAL].append(message)
                app_logic.add_dialogue_thread(
                    'assistant', '\n---\n' + convert_to_openai_style(response)['content'])
                yield
