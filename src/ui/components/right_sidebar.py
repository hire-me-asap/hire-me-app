import gradio as gr

from src.ui.constants import *


class RightSidebar:
    def __init__(self):
        with gr.Sidebar(position='right') as sidebar:
            with gr.Accordion('이력서 미리보기') as resume_preview:
                gr.Markdown('👀👀👀👀👀👀👀')
            with gr.Accordion('아카이브') as archive:
                gr.Chatbot([], type='messages', show_label=False)
        
        self.sidebar = sidebar