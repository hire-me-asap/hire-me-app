import gradio as gr
import re
from pathlib import Path

from ..logic.app_logic import AppLogic

app_logic = AppLogic()

FEATURES = {
    'general': '무엇이든 물어보세요!',
    'job': '직무 찾기',
    'recruit': '채용 공고 찾기',
    'resume': '이력서 검토하기',
    'roadmap': '취업 준비 로드맵 작성하기',
    'course': '강의 찾기'
}

EXAMPLE_MESSAGES = {
    'general': [
        {'text': '🐤 신입에게 적합한 직무나 역할이 뭘까?'},
        {'text': '📛 경력이 없어도 도전할 수 있는 직업에는 어떤 것이 있을까?'},
        {'text': '🛠️ 취업 시장에서 인기가 있는 IT 스킬은 뭘까?'},
        {'text': '📝 이력서에 어떤 IT 관련 경험을 추가하면 취업에 유리할까?'},
    ],
    'job': [
        {'text': '🐤 신입도 취업할 수 있는 일자리가 있을까?'},
        {'text': '🎨 디자인 관련 지식을 살릴 수 있는 직업에는 뭐가 있을까?'},
        {'text': '💻 프론트엔드에 관한 직업에는 뭐가 있을까?'},
        {'text': '🗄️ 백엔드에 관한 경험이 중요한 직업을 추천해줘'},
        {'text': '🤖 인공지능에 관한 지식을 살릴 수 있는 일자리를 찾아줘'},
    ],
    'recruit': [
        {'text': '📢 지금 지원할 수 있는 신입 개발자 채용 공고를 찾아줘.'},
        {'text': '📍 서울 지역에서 프론트엔드 개발자를 뽑는 공고가 있을까?'},
        {'text': '🏢 백엔드 관련 채용 공고를 알려줘.'},
        {'text': '🐍 Python 기술 스택을 주로 사용하는 회사의 공고를 추천해줘.'}, 
    ],
    'resume': [
        {'text': '📄 내 이력서에서 개선할 점이 있을까?'},
        {'text': '🤔 프로젝트 경험을 이력서에 어떻게 녹여내는 것이 좋을까?'},
        {'text': '✨ 신입 개발자로서 이력서에 어떤 내용을 강조해야 할까?'},
    ],
    'roadmap': [
        {'text': '🗺️ 백엔드 개발자가 되기 위한 학습 로드맵을 짜줘.'},
        {'text': '📅 6개월 안에 웹 개발자로 취업하기 위한 계획을 세워줘.'},
        {'text': '📚 비전공자인데 데이터 분석가로 취업하려면 어떤 순서로 공부해야 할까?'},
    ],
    'course': [
        {'text': '🎓 파이썬 기초를 배울 수 있는 온라인 강의를 추천해줘.'},
        {'text': '💻 React 프레임워크 관련해서 평이 좋은 강의가 있을까?'},
        {'text': '💰 무료로 들을 수 있는 데이터베이스 관련 강의를 찾아줘.'},
    ]
}

PROFILE_IMAGE_PLACEHOLDER = 'resources/profile-placeholder.png'


theme = gr.themes.Citrus(
    primary_hue="gray",
    secondary_hue="slate",
    neutral_hue=gr.themes.Color(c100="rgba(245.28242295714108, 245.28242295714108, 246.98289794921874, 1)", c200="rgba(238.76776529924842, 238.76776529924842, 242.56387329101562, 1)", c300="rgba(229.3977127245158, 229.3977127245158, 233.04484863281252, 1)", c400="#bbbbc2", c50="#fafafa", c500="#71717a", c600="#52525b", c700="#3f3f46", c800="#27272a", c900="#18181b", c950="#0f0f11"),
    spacing_size="md",
).set(
    body_background_fill='white',
    body_text_color='*neutral_700',
    embed_radius='*radius_md',
    background_fill_secondary_dark='*neutral_800',
    background_fill_primary_dark='*neutral_900',
    border_color_primary='*neutral_50',
    border_color_primary_dark='*neutral_900',
    color_accent_soft_dark='*neutral_400',
    block_border_width='1px',
    block_background_fill='*neutral_50',
    block_background_fill_dark='*neutral_800',
    block_radius='*radius_md',
    block_title_background_fill='*primary_50',
    block_title_background_fill_dark='*neutral_800',
    layout_gap='*spacing_xl',
    checkbox_background_color='*background_fill_secondary',
    chatbot_text_size='*text_md',
    checkbox_label_background_fill='*neutral_300',
    checkbox_label_background_fill_selected='*secondary_300',
    checkbox_label_border_color_selected='*primary_400',
    table_radius='*radius_md',
    button_medium_text_weight='400',
    button_primary_background_fill='*secondary_200',
    button_primary_background_fill_dark='*primary_800',
    button_primary_text_color='*button_primary_border_color',
    button_primary_text_color_dark='*neutral_300',
    button_secondary_background_fill='*neutral_200',
    button_secondary_background_fill_dark='*primary_400',
    button_secondary_text_color='*primary_500',
    color_accent_soft='*primary_200'
)

gr.set_static_paths(paths=[
    Path.cwd().absolute()/"resources",
    Path.cwd().absolute()/"static",
])

with gr.Blocks(css_paths=['src/ui/style.css'], theme=theme) as demo:
    """ 앱 """
    
    history_state = gr.State([])
    """ State로 history 관리 : 세션 단위의 임시 저장소, 
    이걸 안하면 화면 새로고침 해도 history가 누적 저장됨
    chatbot에서 history 관리시 state를 항상 통과하도록 경로 설정 """

    with gr.Sidebar(position='left') as sidebar:
        """ 사이드바 """

        sidebar_logo_image = gr.Image(
            './resources/logo.png',
            elem_id='sidebar-logo',
            elem_classes=['click_to_home'],
            show_label=False,
            container=False,
            show_download_button=False,
            show_share_button=False,
            show_fullscreen_button=False,
            interactive=False
        )

        profile_button = gr.Button('이력서 입력하러 가기', variant='primary')

        general_chat_button = gr.Button(FEATURES['general'])

        gr.Markdown('📊 맞춤 직무 설계', elem_id='small-title')
        with gr.Group(elem_id='custom-group') :
            job_chat_button = gr.Button(FEATURES['job'], size="md")
            recruit_chat_button = gr.Button(FEATURES['recruit'], size="md")
            resume_chat_button = gr.Button(FEATURES['resume'], size="md")
            roadmap_chat_button = gr.Button(FEATURES['roadmap'], size="md")
            course_chat_button = gr.Button(FEATURES['course'], size="md")

        sidebar_about_image = gr.Image(
            './resources/about.png',
            show_label=False,
            container=False,
            show_download_button=False,
            show_share_button=False,
            show_fullscreen_button=False,
            interactive=False
        )

        sidebar_profile_image = gr.HTML("<img id='profile' src='/gradio_api/file=resources/profile-placeholder.png'>")

    """ 상단 바 """
    with gr.Row(elem_id='topbar-section', visible=False) as topbar:
        topbar_logo_image = gr.Image(
            './resources/logo.png',
            elem_id='topbar-logo',
            show_label=False,
            container=False,
            show_download_button=False,
            show_share_button=False,
            show_fullscreen_button=False
        )

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
            option_checkboxes = gr.CheckboxGroup(
                ['📜 이력서 포함시키기', '이런 식으로 체크박스', '여러 개 넣을 수 있어요'],
                show_label=False,
                elem_id="custom-checkbox"
            )
            input_textarea = gr.TextArea(
                placeholder='❔ 엣취에게 물어보세요',
                lines=1,
                max_lines=5,
                submit_btn=True,
                show_label=False
            )
            gr.Markdown('엣취는 실수를 할 수 있습니다.')

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

    def update_sidebar_profile_image(current):
        if current.endswith("profile-placeholder.png'>") and app_logic._signed_in:
            return gr.HTML(
                f"<img id='profile' src='/gradio_api/file={app_logic.get_user_img(app_logic.user_id())[1:]}'>"
            )
        return gr.update()

    demo.load(update_sidebar_profile_image, inputs=[sidebar_profile_image], outputs=[sidebar_profile_image])
    
    # 로고 보이기 함수 및 이벤트
    def set_topbar_visibility(is_visible):
        return gr.update(visible=is_visible)

    sidebar.expand(lambda: set_topbar_visibility(False), outputs=[topbar])
    sidebar.collapse(lambda: set_topbar_visibility(True), outputs=[topbar])

    # '프로필 입력하러가기' 버튼 클릭 함수 및 이벤트
    def select_profile_tab():
        return gr.update(selected=1)

    profile_button.click(lambda: select_profile_tab(), outputs=[tab_host])

    # chatbot tab 함수 및 이벤트
    def select_chat_tab(mode):
        history = []
        if mode == 'general':
            pass
        elif mode == 'job':
            pass
        elif mode == 'recruit':
            pass
        elif mode == 'resume':
            pass
        elif mode == 'roadmap':
            pass
        elif mode == 'course':
            pass
        else:
            return gr.update(), gr.update()

        return gr.update(selected=0), gr.update(value=history, label=FEATURES[mode], examples=EXAMPLE_MESSAGES[mode])

    general_chat_button.click(lambda: select_chat_tab('general'), outputs=[tab_host, main_chatbot])
    job_chat_button.click(lambda: select_chat_tab('job'), outputs=[tab_host, main_chatbot])
    recruit_chat_button.click(lambda: select_chat_tab('recruit'), outputs=[tab_host, main_chatbot])
    resume_chat_button.click(lambda: select_chat_tab('resume'), outputs=[tab_host, main_chatbot])
    roadmap_chat_button.click(lambda: select_chat_tab('roadmap'), outputs=[tab_host, main_chatbot])
    course_chat_button.click(lambda: select_chat_tab('course'), outputs=[tab_host, main_chatbot])

    # 로고 이미지 클릭시 메인 챗봇으로 이동 이벤트
    topbar_logo_image.select(lambda: select_chat_tab('general'), outputs=[tab_host, main_chatbot])
    sidebar_logo_image.select(lambda: select_chat_tab('general'), outputs=[tab_host, main_chatbot])
    
    def select_example(selected: gr.SelectData):
        return selected.value['text']
    
    main_chatbot.example_select(select_example, outputs=[input_textarea])
    
    def queue_message(content, history):
        if content.strip():
            message = {'role': 'user', 'content': content}
            history.append(message)
        return history
    
    def wait_message(content, history):
        if not content.strip():
            return '', history
        
        response = {'role': 'assistant', 'content': '임시 응답입니다. 엣취!'}
        history.append(response)
        return '', history
    
    input_textarea.submit(
        queue_message, inputs=[input_textarea, main_chatbot], outputs=[main_chatbot]
    ).then(
        wait_message, inputs=[input_textarea, main_chatbot], outputs=[input_textarea, main_chatbot], scroll_to_output=True
    )
    

account_pattern = re.compile(r'^[A-Za-z\d_]{4,}$')

def sign_in_or_sign_up(user_id: str, password: str) -> bool:
    if not account_pattern.fullmatch(user_id) or not account_pattern.fullmatch(password):
        gr.Error('부적절한 아이디 혹은 비밀번호가 입력되었습니다.')
        return False

    logged_in, message = app_logic.sign_in(user_id, password)
    if logged_in:
        return True
    
    if message == '아이디가 존재하지 않습니다.':
        app_logic.sign_up(user_id, password)
        app_logic.sign_in(user_id, password)
        return True
    
    gr.Error('부적절한 아이디 혹은 비밀번호가 입력되었습니다.')
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
