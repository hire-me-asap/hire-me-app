from typing import Any, Optional
import gradio as gr

from src.ui.constants import *
from src.logic.app_logic import app_logic


class RightSidebar:
    def __init__(self):
        with gr.Sidebar(position='right') as sidebar:
            with gr.Accordion('참조 문헌') as citation:
                contents = gr.Markdown('참조 문헌 목록')
            with gr.Accordion('이력서 미리보기') as resume_preview:
                gr.Markdown('👀👀👀👀👀👀👀')
            with gr.Accordion('아카이브') as archive:
                # gr.Chatbot([], type='messages', show_label=False)
                # 갤러리 요소 추가
                self.archive_gallery = gr.Gallery(
                    label="로드맵 이미지",
                    elem_id="archive-gallery",
                    show_label=True
                )
                # 버튼 추가 (로드맵 이미지 로드)
                # self.load_button = gr.Button("로드맵 이미지 로드")

        self.sidebar = sidebar
        self.sidebar.citation = citation
        self.sidebar.citation.contents = contents

    def init_event_handlers(self):
        """
        RightSidebar의 이벤트 핸들러를 초기화합니다.
        """
        pass
