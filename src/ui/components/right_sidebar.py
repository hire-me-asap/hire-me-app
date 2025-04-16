from typing import Any, Optional
import gradio as gr

from src.ui.constants import *


class RightSidebar:
    def __init__(self):
        with gr.Sidebar(position='right') as sidebar:
            with gr.Accordion('참조 문헌') as citation:
                contents = gr.Markdown('참조 문헌 목록')
            with gr.Accordion('이력서 미리보기') as resume_preview:
                gr.Markdown('👀👀👀👀👀👀👀')
            with gr.Accordion('아카이브') as archive:
                gr.Chatbot([], type='messages', show_label=False)

        self.sidebar = sidebar
        self.sidebar.citation = citation
        self.sidebar.citation.contents = contents
