import gradio as gr

from src.ui.constants import *
from src.ui.events import select_chat_tab, select_profile_tab, set_topbar_visibility


class LeftSidebar:
    def __init__(self):
        with gr.Sidebar(position='left') as sidebar:
            # sidebar logo : button에 css 이용하여 이미지 배경 삽입 (gr.HTML 이용시 탭이동 불가, gr.Image 이용시 다크모드 이미지 변경하려면 js 필요)
            # 밝은모드 / 어두운모드 선택시 달라짐 (css로 변경 : 로컬이미지를 css로 불러오기 힘들어서 github에 이미지 올린 후 링크 따옴)
            self.logo_image = gr.Button("", elem_id='sidebar-logo', variant='ghost', size='lg')

            self.profile_button = gr.Button('이력서 입력하러 가기', variant='primary')

            self.general_chat_button = gr.Button(FEATURES[Modes.GENERAL])

            gr.Markdown('📊 맞춤 직무 설계', elem_id='small-title')
            with gr.Group(elem_id='custom-group'):
                self.job_chat_button = gr.Button(FEATURES[Modes.JOB], size="md")
                self.roadmap_chat_button = gr.Button(FEATURES[Modes.ROADMAP], size="md")
                self.recruit_chat_button = gr.Button(FEATURES[Modes.RECRUIT], size="md")
                self.resume_chat_button = gr.Button(FEATURES[Modes.RESUME], size="md")
                self.course_chat_button = gr.Button(FEATURES[Modes.COURSE], size="md")

            # about us : 밝은모드 / 어두운모드 선택시 달라짐 (로컬이미지를 html로 불러오기 힘들어서 github에 이미지 올린 후 링크 따옴)
            gr.HTML("""
                    <picture id="about_us">
                    <source srcset="https://raw.githubusercontent.com/Bosongsae/hiremeasap/refs/heads/main/about_us_white.png" media="(prefers-color-scheme: dark)">
                    <img src="https://raw.githubusercontent.com/Bosongsae/hiremeasap/refs/heads/main/about_us_black.png" style="width: 100%;">
                    </picture>
                    """)

            self.profile_image = gr.HTML("<img id='profile' src='/gradio_api/file=resources/profile-placeholder.png'>")
        
        self.sidebar = sidebar
    
    def init_event_handlers(self, topbar, tab_host, main_chatbot, chat_state):
        # 사이드바 열고 닫을 때
        self.sidebar.expand(lambda: set_topbar_visibility(False), outputs=[topbar])
        self.sidebar.collapse(lambda: set_topbar_visibility(True), outputs=[topbar])

        # '프로필 입력하러가기' 버튼 클릭 함수 및 이벤트
        self.profile_button.click(select_profile_tab, outputs=[tab_host])
        self.profile_image.click(select_profile_tab, outputs=[tab_host])

        # chatbot tab 함수 및 이벤트
        self.general_chat_button.click(
            select_chat_tab, 
            inputs=[gr.State(Modes.GENERAL), chat_state], 
            outputs=[tab_host, main_chatbot, chat_state]
        )
        self.job_chat_button.click(
            select_chat_tab, 
            inputs=[gr.State(Modes.JOB), chat_state], 
            outputs=[tab_host, main_chatbot, chat_state]
        )
        self.recruit_chat_button.click(
            select_chat_tab, 
            inputs=[gr.State(Modes.RECRUIT), chat_state], 
            outputs=[tab_host, main_chatbot, chat_state]
        )
        self.resume_chat_button.click(
            select_chat_tab, 
            inputs=[gr.State(Modes.RESUME), chat_state], 
            outputs=[tab_host, main_chatbot, chat_state]
        )
        self.roadmap_chat_button.click(
            select_chat_tab, 
            inputs=[gr.State(Modes.ROADMAP), chat_state], 
            outputs=[tab_host, main_chatbot, chat_state]
        )
        self.course_chat_button.click(
            select_chat_tab, 
            inputs=[gr.State(Modes.COURSE), chat_state], 
            outputs=[tab_host, main_chatbot, chat_state]
        )
        
        # 로고 이미지 클릭시 메인 챗봇으로 이동 이벤트
        self.logo_image.click(
            select_chat_tab, 
            inputs=[gr.State(None), chat_state], 
            outputs=[tab_host, main_chatbot, chat_state]
        )