import gradio as gr

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
        {'role': 'user', 'text': '🐤 신입에게 적합한 직무나 역할이 뭘까?'},
        {'role': 'user', 'text': '📛 경력이 없어도 도전할 수 있는 직업에는 어떤 것이 있을까?'},
        {'role': 'user', 'text': '🛠️ 취업 시장에서 인기가 있는 IT 스킬은 뭘까?'},
        {'role': 'user', 'text': '📝 이력서에 어떤 IT 관련 경험을 추가하면 취업에 유리할까?'},
    ],
    'job': [
        {'role': 'user', 'text': '🐤 신입도 취업할 수 있는 일자리가 있을까?'},
        {'role': 'user', 'text': '🎨 디자인 관련 지식을 살릴 수 있는 직업에는 뭐가 있을까?'},
        {'role': 'user', 'text': '💻 프론트엔드에 관한 직업에는 뭐가 있을까?'},
        {'role': 'user', 'text': '🗄️ 백엔드에 관한 경험이 중요한 직업을 추천해줘.'},
        {'role': 'user', 'text': '🤖 인공지능에 관한 지식을 살릴 수 있는 일자리를 찾아줘.'},
    ],
    'recruit': [
        {'role': 'user', 'text': '📢 지금 지원할 수 있는 신입 개발자 채용 공고를 찾아줘.'},
        {'role': 'user', 'text': '📍 서울 지역에서 프론트엔드 개발자를 뽑는 공고가 있을까?'},
        {'role': 'user', 'text': '🏢 백엔드 관련 채용 공고를 알려줘.'},
        {'role': 'user', 'text': '🐍 Python 기술 스택을 주로 사용하는 회사의 공고를 추천해줘.'},
    ],
    'resume': [
        {'role': 'user', 'text': '📄 내 이력서에서 개선할 점이 있을까?'},
        {'role': 'user', 'text': '🤔 프로젝트 경험을 이력서에 어떻게 녹여내는 것이 좋을까?'},
        {'role': 'user', 'text': '✨ 신입 개발자로서 이력서에 어떤 내용을 강조해야 할까?'},
    ],
    'roadmap': [
        {'role': 'user', 'text': '🗺️ 백엔드 개발자가 되기 위한 학습 로드맵을 짜줘.'},
        {'role': 'user', 'text': '📅 6개월 안에 웹 개발자로 취업하기 위한 계획을 세워줘.'},
        {'role': 'user', 'text': '📚 비전공자인데 데이터 분석가로 취업하려면 어떤 순서로 공부해야 할까?'},
    ],
    'course': [
        {'role': 'user', 'text': '🎓 파이썬 기초를 배울 수 있는 온라인 강의를 추천해줘.'},
        {'role': 'user', 'text': '💻 React 프레임워크 관련해서 평이 좋은 강의가 있을까?'},
        {'role': 'user', 'text': '💰 무료로 들을 수 있는 데이터베이스 관련 강의를 찾아줘.'},
    ]
}


theme = gr.themes.Citrus(
    primary_hue="slate",
    secondary_hue="rose",
    font='Neo둥근모 Pro',
    font_mono='Neo둥근모 Code'
).set(
    button_large_text_weight=500,
    button_secondary_background_fill='*neutral_200',
    button_secondary_background_fill_hover='*neutral_400',
    button_secondary_background_fill_dark='*neutral_600',
    button_secondary_background_fill_hover_dark='*neutral_900',
    button_cancel_background_fill='*secondary_200',
    button_cancel_background_fill_hover='*secondary_400',
    button_cancel_background_fill_dark='*secondary_600',
    button_cancel_background_fill_hover_dark='*secondary_900',
)


with gr.Blocks(css_paths=['src/tmp/ui-test-style.css'], theme=theme) as demo:
    """ 앱 """

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
        )

        profile_button = gr.Button('이력서 입력하러 가기', variant='primary')

        general_chat_button = gr.Button(FEATURES['general'])

        with gr.Group(elem_id='custom-group'):
            gr.HTML('📊 맞춤 직무 설계')
            job_chat_button = gr.Button(FEATURES['job'])
            recruit_chat_button = gr.Button(FEATURES['recruit'])
            resume_chat_button = gr.Button(FEATURES['resume'])
            roadmap_chat_button = gr.Button(FEATURES['roadmap'])
            course_chat_button = gr.Button(FEATURES['course'])

        sidebar_logo_image = gr.Image(
            './resources/about.png',
            show_label=False,
            container=False,
            show_download_button=False,
            show_share_button=False,
            show_fullscreen_button=False,
        )

        gr.Image(
            './resources/retro_id_card.png',
            elem_id='profile',
            show_label=False,
            container=False,
            show_download_button=False,
            show_share_button=False,
            show_fullscreen_button=False,
        )

    """ 상단 바 """
    with gr.Row(elem_id='topbar-section', visible=False) as topbar:
        topbar_logo_image = gr.Image(
            './resources/logo.png',
            elem_id='topbar-logo',
            show_label=False,
            container=False,
            show_download_button=False,
            show_share_button=False,
            show_fullscreen_button=False,
        )

    with gr.Tabs() as tab_host:
        """ 탭 호스트 """

        with gr.Tab('엣취', id=0, elem_id='chatbot-tab'):
            """ 엣취 탭 """

            with gr.Group() as chat_tab:
                main_chatbot = gr.Chatbot(
                    [],
                    elem_id="chatbot",
                    label=FEATURES['general'],
                    type='messages',
                    examples=EXAMPLE_MESSAGES['general'],
                )
                gr.CheckboxGroup(
                    ['📜 이력서 포함시키기', '이런 식으로 체크박스', '여러 개 넣을 수 있어요'],
                    show_label=False
                )
                gr.TextArea(
                    placeholder='❔ 엣취에게 물어보세요',
                    lines=1,
                    max_lines=5,
                    submit_btn=True,
                    show_label=False
                )
                gr.HTML('엣취는 실수를 할 수 있습니다.')

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

    """ 이벤트 """

    def set_topbar_visibility(is_visible):
        return gr.update(visible=is_visible)

    sidebar.expand(lambda: set_topbar_visibility(False), outputs=[topbar])
    sidebar.collapse(lambda: set_topbar_visibility(True), outputs=[topbar])

    def select_profile_tab():
        return gr.update(selected=1)

    profile_button.click(lambda: select_profile_tab(), outputs=[tab_host])

    def select_chat_tab(mode):
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

        return gr.update(selected=0), gr.update(label=FEATURES[mode], examples=EXAMPLE_MESSAGES[mode])

    general_chat_button.click(lambda: select_chat_tab('general'), outputs=[tab_host, main_chatbot])
    job_chat_button.click(lambda: select_chat_tab('job'), outputs=[tab_host, main_chatbot])
    recruit_chat_button.click(lambda: select_chat_tab('recruit'), outputs=[tab_host, main_chatbot])
    resume_chat_button.click(lambda: select_chat_tab('resume'), outputs=[tab_host, main_chatbot])
    roadmap_chat_button.click(lambda: select_chat_tab('roadmap'), outputs=[tab_host, main_chatbot])
    course_chat_button.click(lambda: select_chat_tab('course'), outputs=[tab_host, main_chatbot])


demo.launch(debug=True)
