import re
import gradio as gr

from pathlib import Path

from src.ui.theme import custom_theme
from src.ui.events import load_histories, update_sidebar_profile_image
from src.ui.constants import *
from src.ui.components import LeftSidebar, RightSidebar, Topbar, TabHost, ProfileTab


gr.set_static_paths(paths=[
    Path.cwd().absolute()/"resources",
    Path.cwd().absolute()/"static",
])

with gr.Blocks(css_paths=['src/ui/style.css'], theme=custom_theme) as demo:

    """ 
    컴포넌트 배치
    """
    left_sidebar_wrapper = LeftSidebar()
    right_sidebar_wrapper = RightSidebar()

    topbar_wrapper = Topbar()
    tab_host_wrapper = TabHost()

    """
    상태 변수
    """

    chat_state = gr.State({
        'mode': Modes.GENERAL,
        'histories': {
            Modes.GENERAL: [],
            Modes.JOB: [],
            Modes.RECRUIT: [],
            Modes.RESUME: [],
            Modes.ROADMAP: [],
            Modes.COURSE: [],
        }
    })

    """
    이벤트 핸들러
    """

    # 앱 처음 실행시
    demo.load(
        update_sidebar_profile_image,
        inputs=[left_sidebar_wrapper.profile_image],
        outputs=[left_sidebar_wrapper.profile_image]
    ).then(
        load_histories,
        inputs=[chat_state],
        outputs=[
            chat_state,
            tab_host_wrapper.chatbot_tab_wrapper.main_chatbot,
            tab_host_wrapper.chatbot_tab_wrapper.input_textarea
        ]
    )
    # 각 컴포넌트의 이벤트 핸들러 초기화
    left_sidebar_wrapper.init_event_handlers(
        topbar_wrapper.topbar,
        tab_host_wrapper.tab_host,
        tab_host_wrapper.chatbot_tab_wrapper.main_chatbot,
        chat_state,
        tab_host_wrapper.profile_tab_wrapper.userid_text,
        tab_host_wrapper.profile_tab_wrapper.profile_image
    )
    topbar_wrapper.init_event_handler(
        chat_state,
        tab_host_wrapper.tab_host,
        tab_host_wrapper.chatbot_tab_wrapper.main_chatbot
    )
    tab_host_wrapper.init_event_handlers(chat_state, right_sidebar_wrapper.sidebar.citation.contents)
