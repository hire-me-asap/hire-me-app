from src.ui.events.on_sidebar_expand_or_collapse import set_topbar_visibility
from src.ui.events.on_chatbot_example_select import select_example
from src.ui.events.on_tab_change_required import select_chat_tab, select_profile_tab
from src.ui.events.on_input_submit import queue_message, wait_message
from src.ui.events.on_demo_load import load_histories, update_sidebar_profile_image
from src.ui.constants import *
from src.ui.theme import custom_theme
from logic.user.app_logic import app_logic
import os
import re
import sys
import gradio as gr

from pathlib import Path

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), "src")))


APP_VERSION = "1.0.0"

gr.set_static_paths(paths=[
    Path.cwd().absolute()/"resources",
    Path.cwd().absolute()/"static",
])

with gr.Blocks(css_paths=['src/ui/style.css'], theme=custom_theme) as demo:
    """ 앱 """

    with gr.Sidebar(position='left') as sidebar:
        # sidebar logo : button에 css 이용하여 이미지 배경 삽입 (gr.HTML 이용시 탭이동 불가, gr.Image 이용시 다크모드 이미지 변경하려면 js 필요)
        # 밝은모드 / 어두운모드 선택시 달라짐 (css로 변경 : 로컬이미지를 css로 불러오기 힘들어서 github에 이미지 올린 후 링크 따옴)
        sidebar_logo_image = gr.Button(
            "", elem_id='sidebar-logo', variant='ghost', size='lg')

        profile_button = gr.Button('이력서 입력하러 가기', variant='primary')

        general_chat_button = gr.Button(FEATURES[Modes.GENERAL])

        gr.Markdown('📊 맞춤 직무 설계', elem_id='small-title')
        with gr.Group(elem_id='custom-group'):
            job_chat_button = gr.Button(FEATURES[Modes.JOB], size="md")
            roadmap_chat_button = gr.Button(FEATURES[Modes.ROADMAP], size="md")
            recruit_chat_button = gr.Button(FEATURES[Modes.RECRUIT], size="md")
            resume_chat_button = gr.Button(FEATURES[Modes.RESUME], size="md")
            course_chat_button = gr.Button(FEATURES[Modes.COURSE], size="md")

        # about us : 밝은모드 / 어두운모드 선택시 달라짐 (로컬이미지를 html로 불러오기 힘들어서 github에 이미지 올린 후 링크 따옴)
        gr.HTML("""
                <picture id="about_us">
                <source srcset="https://raw.githubusercontent.com/Bosongsae/hiremeasap/refs/heads/main/about_us_white.png" media="(prefers-color-scheme: dark)">
                <img src="https://raw.githubusercontent.com/Bosongsae/hiremeasap/refs/heads/main/about_us_black.png" style="width: 100%;">
                </picture>
                """)

        sidebar_profile_image = gr.HTML(
            "<img id='profile' src='/gradio_api/file=resources/profile-placeholder.png'>")

    with gr.Sidebar(position='right') as sidebar2:
        with gr.Accordion('이력서 미리보기') as resume_preview:
            gr.Markdown('👀👀👀👀👀👀👀')
        with gr.Accordion('아카이브') as archive:
            gr.Chatbot([], type='messages', show_label=False)

    """ 상단 바 """
    with gr.Row(elem_id='topbar-section', visible=False) as topbar:
        # topbar logo : button에 css 이용하여 이미지 배경 삽입 (gr.HTML 이용시 탭이동 불가, gr.Image 이용시 다크모드 이미지 변경하려면 js 필요)
        # 밝은모드 / 어두운모드 선택시 달라짐 (css로 변경 : 로컬이미지를 css로 불러오기 힘들어서 github에 이미지 올린 후 링크 따옴)
        topbar_logo_image = gr.Button(
            "", elem_id='topbar-logo', variant='ghost', size='lg')

    with gr.Tabs() as tab_host:
        """ 탭 호스트 """

        with gr.Tab('엣취', id=0, elem_id='chatbot-tab'):
            """ 엣취 탭 """

            main_chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                label=FEATURES[Modes.GENERAL],
                type='messages',
                examples=EXAMPLE_MESSAGES[Modes.GENERAL],
            )
            user_check = gr.CheckboxGroup(
                ['📜 이력서 포함시키기', '이런 식으로 체크박스', '여러 개 넣을 수 있어요'],
                show_label=False,
                elem_id="custom-checkbox"
            )
            input_textarea = gr.TextArea(
                placeholder='❔ 엣취에게 물어보세요',
                elem_id='user-input-txt',
                lines=1,
                max_lines=5,
                submit_btn=True,
                show_label=False
            )
            gr.Markdown('엣취는 실수를 할 수 있습니다.', elem_id='etch_kawai')

        with gr.Tab('프로필', id=1) as profile_tab:
            """ 프로필 탭 """

            gr.Markdown('# 💳 사용자 정보 관리')

            with gr.Row():
                with gr.Column(scale=4):
                    username_text = gr.Text(
                        label='사용자 이름',
                        placeholder='사용자 ID가 표시됩니다',
                        interactive=False
                    )
                    preferred_job = gr.Text(
                        label='희망 직무',
                        placeholder='희망하는 직무를 입력해보세요'
                    )
                    gr.Button('변경사항 저장하기', variant='primary',
                              elem_classes=['profile-save-button'])

                with gr.Column():
                    profile_image = gr.Image(interactive=False, scale=1)

            gr.Markdown()
            gr.Markdown('# 📜 이력서 관리')

            with gr.Group():
                user_skill_dropdown = gr.Dropdown(
                    ['기술1', '기술2', '기술3'],
                    label='스킬 셋',
                    multiselect=True
                )
                with gr.Row():
                    education_level_dropdown = gr.Dropdown(
                        [
                            '초등학교 졸업', '중학교 졸업', '고등학교 졸업',
                            '검정고시 합격', '학사 학위', '석사 학위', '박사 학위'
                        ],
                        label='최종 학력',
                        multiselect=False,
                        interactive=True
                    )
                    major_textbox = gr.Textbox(
                        label='전공',
                        placeholder='전공명을 적으세요'
                    )
                additional_educations_textbox = gr.TextArea(
                    label='교육사항',
                    placeholder='지원하고자 하는 직무와 관련하여 이수했던 교육들을 나열해주세요'
                )
                user_resume_textbox = gr.TextArea(
                    label='경력사항',
                    placeholder='지원하고자 하는 직무와 관련된 업무 경험 및 활동 경험들을 나열해주세요'
                )
                user_resume_textbox = gr.TextArea(
                    label='추가적인 정보',
                    placeholder='엣취가 당신에 대해 이해하기 위해 필요한 추가적인 정보를 자유롭게 적어주세요'
                )

            gr.Button('변경사항 저장하기', variant='primary',
                      elem_classes=['profile-save-button'])
            gr.Markdown()

            with gr.Accordion('⚠️ 위험한 기능', open=False):
                gr.Markdown()

                gr.Markdown(
                    '프로필 페이지에 입력된 이력서를 모두 빈칸으로 되돌립니다. 이 작업은 되돌릴 수 없습니다.')
                clear_resume_button = gr.Button(
                    '이력서 지우기', elem_classes='red-button')
                gr.Markdown()

                gr.Markdown('사용자의 모든 대화 기록을 지웁니다. 이 작업은 되돌릴 수 없습니다.')
                clear_history_button = gr.Button(
                    '대화 기록 지우기', elem_classes='red-button')

    gr.Markdown("""
        <div id="site-footer">
                © 2025 hire me ASAP Inc. ·
                ✉️ contact@hiremeasap.com ·
                <a href="https://github.com/hire-me-asap" target="_blank" style="color:#d5d5d5;">github.com/hire-me-asap</a> ·
                <a href="#" style="color:#d5d5d5;">Privacy Policy</a>
                </div>
            """)

    """ 이벤트 """
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

    """ 이벤트 핸들러 """

    # 앱 처음 실행시
    demo.load(
        update_sidebar_profile_image, inputs=[
            sidebar_profile_image], outputs=[sidebar_profile_image]
    ).then(
        load_histories, inputs=[chat_state], outputs=[
            chat_state, main_chatbot, input_textarea]
    )

    # 사이드바 열고 닫을 때
    sidebar.expand(lambda: set_topbar_visibility(False), outputs=[topbar])
    sidebar.collapse(lambda: set_topbar_visibility(True), outputs=[topbar])

    # '프로필 입력하러가기' 버튼 클릭 함수 및 이벤트
    profile_button.click(select_profile_tab, outputs=[tab_host])
    sidebar_profile_image.click(select_profile_tab, outputs=[tab_host])

    # chatbot tab 함수 및 이벤트
    general_chat_button.click(
        select_chat_tab,
        inputs=[gr.State(Modes.GENERAL), chat_state],
        outputs=[tab_host, main_chatbot, chat_state]
    )
    job_chat_button.click(
        select_chat_tab,
        inputs=[gr.State(Modes.JOB), chat_state],
        outputs=[tab_host, main_chatbot, chat_state]
    )
    recruit_chat_button.click(
        select_chat_tab,
        inputs=[gr.State(Modes.RECRUIT), chat_state],
        outputs=[tab_host, main_chatbot, chat_state]
    )
    resume_chat_button.click(
        select_chat_tab,
        inputs=[gr.State(Modes.RESUME), chat_state],
        outputs=[tab_host, main_chatbot, chat_state]
    )
    roadmap_chat_button.click(
        select_chat_tab,
        inputs=[gr.State(Modes.ROADMAP), chat_state],
        outputs=[tab_host, main_chatbot, chat_state]
    )
    course_chat_button.click(
        select_chat_tab,
        inputs=[gr.State(Modes.COURSE), chat_state],
        outputs=[tab_host, main_chatbot, chat_state]
    )

    # 로고 이미지 클릭시 메인 챗봇으로 이동 이벤트
    topbar_logo_image.click(
        select_chat_tab,
        inputs=[gr.State(None), chat_state],
        outputs=[tab_host, main_chatbot, chat_state]
    )
    sidebar_logo_image.click(
        select_chat_tab,
        inputs=[gr.State(None), chat_state],
        outputs=[tab_host, main_chatbot, chat_state]
    )

    # 챗봇 예시 메시지 클릭 -> 입력 텍스트 박스 값으로 전달
    main_chatbot.example_select(select_example, outputs=[input_textarea])

    input_textarea.submit(
        queue_message,
        inputs=[input_textarea, chat_state],
        outputs=[main_chatbot, chat_state]
    ).then(
        wait_message,
        inputs=[input_textarea, chat_state],
        outputs=[input_textarea, main_chatbot, chat_state],
        scroll_to_output=True
    )


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
