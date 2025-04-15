from typing import Optional
import gradio as gr
import re
from pathlib import Path
from enum import Enum
from theme import custom_theme
from ..logic.app_logic import app_logic, AssistantType
from ..logic.messages import convert_to_openai_style


class Modes(Enum):
    GENERAL = "general"
    JOB = "job"
    RECRUIT = "recruit"
    RESUME = "resume"
    ROADMAP = "roadmap"
    COURSE = "course"


ASSISTANTS_OF_MODE = {
    Modes.GENERAL: AssistantType.ASSISTANT,
    Modes.JOB: AssistantType.JOB_RECOMMEND,
    Modes.RECRUIT: AssistantType.RECRUIT_RECOMMEND,
    Modes.RESUME: AssistantType.RESUME_REVIEW,
    Modes.ROADMAP: AssistantType.ROADMAP,
    Modes.COURSE: AssistantType.FIND_STUDY,
}

FEATURES = {
    Modes.GENERAL: '무엇이든 물어보세요!',
    Modes.JOB: '직무 찾기',
    Modes.RECRUIT: '채용 공고 찾기',
    Modes.RESUME: '이력서 검토하기',
    Modes.ROADMAP: '취업 준비 로드맵 작성하기',
    Modes.COURSE: '강의 찾기'
}

EXAMPLE_MESSAGES = {
    Modes.GENERAL: [
        {'text': '🐤 신입에게 적합한 직무나 역할이 뭘까?'},
        {'text': '📛 경력이 없어도 도전할 수 있는 직업에는 어떤 것이 있을까?'},
        {'text': '🛠️ 취업 시장에서 인기가 있는 IT 스킬은 뭘까?'},
        {'text': '📝 이력서에 어떤 IT 관련 경험을 추가하면 취업에 유리할까?'},
    ],
    Modes.JOB: [
        {'text': '🐤 신입도 취업할 수 있는 일자리가 있을까?'},
        {'text': '🎨 디자인 관련 지식을 살릴 수 있는 직업에는 뭐가 있을까?'},
        {'text': '💻 프론트엔드에 관한 직업에는 뭐가 있을까?'},
        {'text': '🗄️ 백엔드에 관한 경험이 중요한 직업을 추천해줘'},
        {'text': '🤖 인공지능에 관한 지식을 살릴 수 있는 일자리를 찾아줘'},
    ],
    Modes.RECRUIT: [
        {'text': '📢 지금 지원할 수 있는 신입 개발자 채용 공고를 찾아줘.'},
        {'text': '📍 서울 지역에서 프론트엔드 개발자를 뽑는 공고가 있을까?'},
        {'text': '🏢 백엔드 관련 채용 공고를 알려줘.'},
        {'text': '🐍 Python 기술 스택을 주로 사용하는 회사의 공고를 추천해줘.'}, 
    ],
    Modes.RESUME: [
        {'text': '📄 내 이력서에서 개선할 점이 있을까?'},
        {'text': '🤔 프로젝트 경험을 이력서에 어떻게 녹여내는 것이 좋을까?'},
        {'text': '✨ 신입 개발자로서 이력서에 어떤 내용을 강조해야 할까?'},
    ],
    Modes.ROADMAP: [
        {'text': '🗺️ 백엔드 개발자가 되기 위한 학습 로드맵을 짜줘.'},
        {'text': '📅 6개월 안에 웹 개발자로 취업하기 위한 계획을 세워줘.'},
        {'text': '📚 비전공자인데 데이터 분석가로 취업하려면 어떤 순서로 공부해야 할까?'},
    ],
    Modes.COURSE: [
        {'text': '🎓 파이썬 기초를 배울 수 있는 온라인 강의를 추천해줘.'},
        {'text': '💻 React 프레임워크 관련해서 평이 좋은 강의가 있을까?'},
        {'text': '💰 무료로 들을 수 있는 데이터베이스 관련 강의를 찾아줘.'},
    ]
}

PROFILE_IMAGE_PLACEHOLDER = 'resources/profile-placeholder.png'


gr.set_static_paths(paths=[
    Path.cwd().absolute()/"resources",
    Path.cwd().absolute()/"static",
])

with gr.Blocks(css_paths=['src/ui/style.css'], theme=custom_theme) as demo:
    """ 앱 """
        
    with gr.Sidebar(position='left') as sidebar:
        
        # sidebar logo : button에 css 이용하여 이미지 배경 삽입 (gr.HTML 이용시 탭이동 불가, gr.Image 이용시 다크모드 이미지 변경하려면 js 필요)
        # 밝은모드 / 어두운모드 선택시 달라짐 (css로 변경 : 로컬이미지를 css로 불러오기 힘들어서 github에 이미지 올린 후 링크 따옴)
        sidebar_logo_image = gr.Button("", elem_id='sidebar-logo', variant='ghost', size='lg')
        
        profile_button = gr.Button('이력서 입력하러 가기', variant='primary')

        general_chat_button = gr.Button(FEATURES['general'])
        
        gr.Markdown('📊 맞춤 직무 설계', elem_id='small-title')
        with gr.Group(elem_id='custom-group') :
            job_chat_button = gr.Button(FEATURES['job'], size="md")
            roadmap_chat_button = gr.Button(FEATURES['roadmap'], size="md")
            recruit_chat_button = gr.Button(FEATURES['recruit'], size="md")
            resume_chat_button = gr.Button(FEATURES['resume'], size="md")            
            course_chat_button = gr.Button(FEATURES['course'], size="md")

        # about us : 밝은모드 / 어두운모드 선택시 달라짐 (로컬이미지를 html로 불러오기 힘들어서 github에 이미지 올린 후 링크 따옴)
        gr.HTML("""
                <picture id="about_us">
                <source srcset="https://raw.githubusercontent.com/Bosongsae/hiremeasap/refs/heads/main/about_us_white.png" media="(prefers-color-scheme: dark)">
                <img src="https://raw.githubusercontent.com/Bosongsae/hiremeasap/refs/heads/main/about_us_black.png" style="width: 100%;">
                </picture>
                """)

        sidebar_profile_image = gr.Image(
            './resources/retro_id_card.png',
            elem_id='profile',
            show_label=False,
            container=False,
            show_download_button=False,
            show_share_button=False,
            show_fullscreen_button=False,
        )

        sidebar_profile_image = gr.HTML("<img id='profile' src='/gradio_api/file=resources/profile-placeholder.png'>")


    with gr.Sidebar(position='right') as sidebar2:
        with gr.Accordion('이력서 미리보기') as resume_preview:
            gr.Markdown('👀👀👀👀👀👀👀')
        with gr.Accordion('아카이브') as archive:
            gr.Chatbot([], type='messages', show_label=False)
        
        
    """ 상단 바 """
    with gr.Row(elem_id='topbar-section', visible=False) as topbar:
        # topbar logo : button에 css 이용하여 이미지 배경 삽입 (gr.HTML 이용시 탭이동 불가, gr.Image 이용시 다크모드 이미지 변경하려면 js 필요)
        # 밝은모드 / 어두운모드 선택시 달라짐 (css로 변경 : 로컬이미지를 css로 불러오기 힘들어서 github에 이미지 올린 후 링크 따옴)
        topbar_logo_image = gr.Button("", elem_id='topbar-logo', variant='ghost', size='lg')

    with gr.Tabs() as tab_host:
        """ 탭 호스트 """

        with gr.Tab('엣취', id=0, elem_id='chatbot-tab'):
            """ 엣취 탭 """
            
            main_chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                label=FEATURES['general'],
                type='messages',
                examples=EXAMPLE_MESSAGES['general'],
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
                    gr.Button('변경사항 저장하기', variant='primary', elem_classes=['profile-save-button'])

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
                
            gr.Button('변경사항 저장하기', variant='primary', elem_classes=['profile-save-button'])
            gr.Markdown()
            
            with gr.Accordion('⚠️ 위험한 기능', open=False):
                gr.Markdown()
                
                gr.Markdown('프로필 페이지에 입력된 이력서를 모두 빈칸으로 되돌립니다. 이 작업은 되돌릴 수 없습니다.')                
                clear_resume_button = gr.Button('이력서 지우기', variant='stop')
                gr.Markdown()

                gr.Markdown('사용자의 모든 대화 기록을 지웁니다. 이 작업은 되돌릴 수 없습니다.')
                clear_history_button = gr.Button('대화 기록 지우기', variant='stop')
    
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

    def update_sidebar_profile_image(current):
        if not app_logic.signed_in():
            return gr.update()
        
        if not current.endswith("profile-placeholder.png'>"):
            return gr.update()
        
        return gr.HTML(
            f"<img id='profile' src='/gradio_api/file={app_logic.get_user_img()[1:]}'>"
        )
    
    def load_histories(chat_state):
        if not app_logic.signed_in():
            return gr.update(), gr.update()
        
        for mode in Modes:
            history = app_logic.get_all_thread_dialogue(ASSISTANTS_OF_MODE[mode])
            chat_state['histories'][mode] = list(map(convert_to_openai_style, reversed(history)))
        
        return chat_state, chat_state['histories'][chat_state['mode']], ''

    demo.load(
        update_sidebar_profile_image, inputs=[sidebar_profile_image], outputs=[sidebar_profile_image]
    ).then(
        load_histories, inputs=[chat_state], outputs=[chat_state, main_chatbot, input_textarea]
    )
    
    # 로고 보이기 함수 및 이벤트
    def set_topbar_visibility(is_visible):
        return gr.update(visible=is_visible)

    sidebar.expand(lambda: set_topbar_visibility(False), outputs=[topbar])
    sidebar.collapse(lambda: set_topbar_visibility(True), outputs=[topbar])

    # '프로필 입력하러가기' 버튼 클릭 함수 및 이벤트
    def select_profile_tab():
        return gr.update(selected=1)

    profile_button.click(lambda: select_profile_tab(), outputs=[tab_host])
    sidebar_profile_image.select(lambda: select_profile_tab(), outputs=[tab_host]) ## Image 요소라서 click으로 안됨 

    # chatbot tab 함수 및 이벤트
    def select_chat_tab(mode: Optional[Modes], chat_state):
        mode = mode if mode else chat_state['mode']
        chat_state['mode'] = mode
        return gr.update(selected=0), gr.update(value=chat_state['histories'][mode], label=FEATURES[mode], examples=EXAMPLE_MESSAGES[mode]), chat_state

    general_chat_button.click(select_chat_tab, inputs=[gr.State(Modes.GENERAL), chat_state], outputs=[tab_host, main_chatbot, chat_state])
    job_chat_button.click(select_chat_tab, inputs=[gr.State(Modes.JOB), chat_state], outputs=[tab_host, main_chatbot, chat_state])
    recruit_chat_button.click(select_chat_tab, inputs=[gr.State(Modes.RECRUIT), chat_state], outputs=[tab_host, main_chatbot, chat_state])
    resume_chat_button.click(select_chat_tab, inputs=[gr.State(Modes.RESUME), chat_state], outputs=[tab_host, main_chatbot, chat_state])
    roadmap_chat_button.click(select_chat_tab, inputs=[gr.State(Modes.ROADMAP), chat_state], outputs=[tab_host, main_chatbot, chat_state])
    course_chat_button.click(select_chat_tab, inputs=[gr.State(Modes.COURSE), chat_state], outputs=[tab_host, main_chatbot, chat_state])

    # 로고 이미지 클릭시 메인 챗봇으로 이동 이벤트
    topbar_logo_image.click(select_chat_tab, inputs=[gr.State(None), chat_state], outputs=[tab_host, main_chatbot, chat_state])
    sidebar_logo_image.click(select_chat_tab, inputs=[gr.State(None), chat_state], outputs=[tab_host, main_chatbot, chat_state])

    def select_example(selected: gr.SelectData):
        return selected.value['text']

    main_chatbot.example_select(select_example, outputs=[input_textarea])

    def queue_message(content, chat_state):
        if content.strip():
            message = {'role': 'user', 'content': content}
            chat_state['histories'][chat_state['mode']].append(message)
            chat_state['histories'][chat_state['mode']].append({'role': 'assistant', 'content': '허리 피세요'})
        return chat_state['histories'][chat_state['mode']], chat_state
    
    def wait_message(content, chat_state):
        mode = chat_state['mode']
        if not content.strip():
            return '', chat_state['histories'][mode], chat_state

        response = app_logic.get_response_from_assistant(
            ASSISTANTS_OF_MODE[mode],
            content
        )
        message = convert_to_openai_style(response)
        chat_state['histories'][mode].pop()
        chat_state['histories'][mode].append(message)
        return '', chat_state['histories'][chat_state['mode']], chat_state
    
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
