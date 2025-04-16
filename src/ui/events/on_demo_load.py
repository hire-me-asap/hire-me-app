import gradio as gr

from src.ui.constants import ASSISTANTS_OF_MODE, Modes
from src.logic.app_logic import app_logic
from src.ui.messages import convert_to_openai_style, convert_general_response_to_openai_style, convert_roadmap_to_openai_style


def update_sidebar_profile_image(current):
    if not app_logic.signed_in():
        return gr.update()

    if not current.endswith("profile-placeholder.png'>"):
        return gr.update()

    return gr.HTML(
        f"<img id='profile' src='/gradio_api/file={app_logic.get_user_img()[1:]}'>"
    )


def load_histories(chat_state):
    if not app_logic.signed_in():
        return gr.update(), gr.update()

    for mode in Modes:
        history = app_logic.get_all_thread_dialogue(
            ASSISTANTS_OF_MODE[mode])
        if mode == Modes.GENERAL:
            def converter(
                r): return convert_general_response_to_openai_style(r)[0]
        elif mode == Modes.ROADMAP:
            converter = convert_roadmap_to_openai_style
        else:
            converter = convert_to_openai_style
        chat_state['histories'][mode] = list(map(converter, reversed(history)))

    return chat_state, chat_state['histories'][chat_state['mode']], ''
