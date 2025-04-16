from typing import Optional
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
    
    def get_vector_store_file_id_list(annotations: list[dict]) -> Optional[list[str]]:
        """annotations 의 형식은 다음과 같이 생겼음.\n
        annotations = [{
            'type': 'file_citation',
            'text': '【4:0†source】',
            'start_index': 548,
            'end_index': 560,
            'file_citation': {'file_id': 'assistant-****'}}
        ]

        Args:
            annotations (list[dict]): 참조 목록

        Returns:
            list[str]: vector store file id
        """
        if annotations:
            return [annotation['file_citation']['file_id'] for annotation in annotations]
        else:
            return None
            # return '선택한 항목에 대한 참조 문헌이 없습니다.'
