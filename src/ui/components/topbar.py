import gradio as gr

from src.ui.events import select_chat_tab


class Topbar:
    def __init__(self):
        with gr.Row(elem_id='topbar-section', visible=False) as topbar:
            # topbar logo : button에 css 이용하여 이미지 배경 삽입 (gr.HTML 이용시 탭이동 불가, gr.Image 이용시 다크모드 이미지 변경하려면 js 필요)
            # 밝은모드 / 어두운모드 선택시 달라짐 (css로 변경 : 로컬이미지를 css로 불러오기 힘들어서 github에 이미지 올린 후 링크 따옴)
            self.logo_image = gr.Button("", elem_id='topbar-logo', variant='ghost', size='lg')

        self.topbar = topbar

    def init_event_handler(self, chat_state, tab_host, main_chatbot):
        self.logo_image.click(
            select_chat_tab, 
            inputs=[gr.State(None), chat_state], 
            outputs=[tab_host, main_chatbot, chat_state]
        )
