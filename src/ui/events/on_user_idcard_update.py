import gradio as gr 
from src.logic.app_logic import app_logic

def id_card_update() :
    return gr.HTML(f"<img id='profile' src='/gradio_api/file={app_logic.get_user_img()[1:]}'>"), gr.HTML(
        f"<img id='profile' src='/gradio_api/file={app_logic.get_user_img()[1:]}'>")