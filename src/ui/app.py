import re
import gradio as gr

from pathlib import Path

from src.logic.app_logic import app_logic
from src.ui.theme import custom_theme
from src.ui.events import load_histories, update_sidebar_profile_image
from src.ui.constants import *
from src.ui.components import LeftSidebar, RightSidebar, Topbar, TabHost

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

    gr.Markdown("""
        <div id="site-footer">
            © 2025 hire me ASAP Inc. ·
            ✉️ contact@hiremeasap.com ·
            <a href="https://github.com/hire-me-asap" target="_blank" style="color:#d5d5d5;">github.com/hire-me-asap</a> ·
            <a href="#" style="color:#d5d5d5;">Privacy Policy</a>
        </div>
    """)

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
        chat_state
    )
    topbar_wrapper.init_event_handler(
        chat_state,
        tab_host_wrapper.tab_host,
        tab_host_wrapper.chatbot_tab_wrapper.main_chatbot
    )
    tab_host_wrapper.init_event_handlers(chat_state)


account_pattern = re.compile(r'^[A-Za-z\d_]{4,}$')


def sign_in_or_sign_up(user_id: str, password: str) -> bool:
    if not account_pattern.fullmatch(user_id) or not account_pattern.fullmatch(password):
        return False

    logged_in, message = app_logic.sign_in(user_id, password)
    if logged_in:
        return True

    if message == '아이디가 존재하지 않습니다.':
        app_logic.sign_up(user_id, password)
        return True

    return False


AUTH_MESSAGE = (
    '<p><b>새 계정</b>으로 가입하거나 <b>기존 계정</b>으로 로그인하세요.</p><p><nbsp></p>'
    '<p>&#8203;</p>'
    '<p>아이디와 비밀번호는 <b>길이가 4 이상</b>이어야 하고<br/>'
    '<b>영문자, 숫자, 언더바</b>로만 구성되어야 합니다.</p>'
    '<p>&#8203;</p>'
    '<p><b>[로그인]</b> 버튼을 클릭하고 잠시 기다려주세요</p>'
    '<p>첫 가입 시에는 리소스 할당에 1분 정도 소요될 수 있습니다.</p>'
)
