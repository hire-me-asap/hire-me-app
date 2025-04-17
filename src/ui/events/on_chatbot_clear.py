import gradio as gr 
from src.ui.constants import *

def clear_history():
    initial_chat_state = {
        'mode': Modes.GENERAL,
        'histories': {
            Modes.GENERAL: [],
            Modes.JOB: [],
            Modes.RECRUIT: [],
            Modes.RESUME: [],
            Modes.ROADMAP: [],
            Modes.COURSE: [],
        },
        'use_resume': True
    }
    return gr.update(value=initial_chat_state['histories'][Modes.GENERAL]), gr.update(value=initial_chat_state['histories'][Modes.GENERAL])