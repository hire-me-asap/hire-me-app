import gradio as gr
from typing import Optional
from src.logic.app_logic import app_logic
from src.ui.constants import EXAMPLE_MESSAGES, FEATURES, Modes


def select_profile_tab():
    return gr.update(selected=1), gr.update(value=app_logic.user_id())


def select_chat_tab(mode: Optional[Modes], chat_state):
    mode = mode if mode else chat_state['mode']
    chat_state['mode'] = mode
    return (
        gr.update(selected=0),
        gr.update(
            value=chat_state['histories'][mode],
            label=FEATURES[mode],
            examples=EXAMPLE_MESSAGES[mode]
        ),
        chat_state
    )
