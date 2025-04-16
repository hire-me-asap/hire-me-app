import gradio as gr

from src.logic.app_logic import app_logic
from src.ui.messages import convert_to_openai_style, convert_general_response_to_openai_style
from src.ui.constants import ASSISTANTS_OF_MODE, Modes


PROGRESS_MESSAGE = {'role': 'assistant', 'content': '🤧💭 엣취가 답변을 생각하고 있습니다. *허리를 쭉 피세요!!!*'}


def process_user_message(content, chat_state):
    mode = chat_state['mode']
    content = content.strip()
    if not content:
        yield gr.update(), gr.update(), gr.update()
        return
    
    message = {'role': 'user', 'content': content}
    chat_state['histories'][mode].append(message)
    chat_state['histories'][mode].append(PROGRESS_MESSAGE)
    
    yield '', chat_state['histories'][chat_state['mode']], chat_state

    chat_state['histories'][mode].pop()  # 허리피세요
    
    for _ in _get_assistant_response(content, mode, chat_state):
        yield '', chat_state['histories'][chat_state['mode']], chat_state
            

def _get_assistant_response(content: str, mode: Modes, chat_state):
    print(f'@_get_assistant_response({content=}, {mode=}, chat_state)')
    
    response = app_logic.get_response_from_assistant(
        ASSISTANTS_OF_MODE[mode],
        content
    )
    
    if mode != Modes.GENERAL:
        message = convert_to_openai_style(response)
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
            chat_state['histories'][mode].append({'role': 'user', 'content': content})
            
            chat_state['histories'][Modes.GENERAL].append(PROGRESS_MESSAGE)
            yield
            chat_state['histories'][Modes.GENERAL].pop()
            
            for message, response in _get_assistant_response(query, mode, chat_state):
                message['content'] = '\n---\n' + message['content']
                chat_state['histories'][Modes.GENERAL].append(message)
                app_logic.add_dialogue_thread('assistant', '\n---\n' + convert_to_openai_style(response)['content'])
                yield