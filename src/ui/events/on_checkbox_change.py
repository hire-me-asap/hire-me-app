from src.ui.constants import INCLUDE_RESUME


def toggle_resume_usage(selected: list[str], chat_state):    
    chat_state['use_resume'] = INCLUDE_RESUME in selected
    return chat_state