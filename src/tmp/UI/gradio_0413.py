import gradio as gr
import base64

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
    ]
}
    

theme = gr.themes.Soft(
    primary_hue="slate",
    secondary_hue="stone",
    neutral_hue="zinc",
    
).set(
    button_large_text_weight=400,
    block_title_text_weight=400,
)



# gr.HTML 에서 로컬 디렉토리 파일을 못불러오기 때문에 따로 불러와줌 
with open("logo.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")
# 주소 설정 
img_html = f'<img src="data:image/png;base64,{image_data}">'


with gr.Blocks(css_paths=['gradio_0413_style.css'], theme=theme) as demo:
    """ 앱 """
    
    history_state = gr.State([])
    """ State로 history 관리 : 세션 단위의 임시 저장소, 
    이걸 안하면 화면 새로고침 해도 history가 누적 저장됨
    chatbot에서 history 관리시 state를 항상 통과하도록 경로 설정 """

    with gr.Sidebar(position='left') as sidebar:
        """ 사이드바 """

        sidebar_logo_image = gr.Image(
            'logo.png',
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
            'about.png',
            show_label=False,
            container=False,
            show_download_button=False,
            show_share_button=False,
            show_fullscreen_button=False,
        )

        """ Profile + login """        
        profile = gr.Markdown("👤 프로필", elem_id='profile')
        profile_img = gr.Image(
                'retro_id_card.png',
                show_label=False,
                container=False,
                show_download_button=False,
                show_share_button=False,
                show_fullscreen_button=False,                
            )

    """ 상단 로고 """
    with gr.Row(elem_id='topbar-section', visible=False) as topbar:
        top_logo = gr.HTML(f"""<div id="topbar-logo" style="text-align: center; cursor: pointer;">{img_html}</div>""")
        
        # topbar_logo_image = gr.Image(
        #     './resources/logo.png',
        #     elem_id='topbar-logo',
        #     show_label=False,
        #     container=False,
        #     show_download_button=False,
        #     show_share_button=False,
        #     show_fullscreen_button=False,
        # )

    with gr.Tabs() as tab_host:
        """ 탭 호스트 """

        with gr.Tab('엣취', id=0, elem_id='chatbot-tab'):
            """ 엣취 탭 """

            with gr.Group(elem_id='chatbot_group') as chat_tab:
                main_chatbot = gr.Chatbot(
                    [],
                    elem_id="chatbot",
                    label=FEATURES['general'],
                    type='messages',
                    examples=EXAMPLE_MESSAGES['general'],
                )
                user_check = gr.CheckboxGroup(
                    ['📜 이력서 포함시키기', '선택1', '선택2'],
                    show_label=False,
                    elem_id="custom-checkbox"
                )
                user_input = gr.TextArea(
                    placeholder='❔ 엣취에게 물어보세요',
                    lines=1,
                    max_lines=5,
                    submit_btn=True,
                    show_label=False
                )
                gr.HTML('엣취는 실수를 할 수 있습니다.')

        with gr.Tab('프로필', id=1) as profile_tab:
            """ 프로필 탭 """

            gr.Markdown('### 사용자 정보 관리')

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

                with gr.Column():
                    profile_image = gr.Image(interactive=False, scale=1)

            gr.Markdown('### 이력서 관리')

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
                    label='그 밖의 교육',
                    placeholder='이수했던 교육을 추가로 설명해보세요'
                )
                user_resume_textbox = gr.TextArea(
                    label='이력서',
                    placeholder='직무 관련 경험을 입력해주세요'
                )
                user_resume_textbox = gr.TextArea(
                    label='이력서',
                    placeholder='직무 관련 경험을 입력해주세요'
                )

            gr.Button('변경사항 저장하기', variant='primary')

            with gr.Accordion('⚠️ 위험한 기능', open=False):
                clear_history_button = gr.Button(
                    '모든 사용 기록 지우기', variant='stop')


    gr.Markdown("""
        <div id="site-footer">
                © 2025 hire me ASAP Inc. ·
                ✉️ contact@hiremeasap.com ·
                <a href="https://github.com/hire-me-asap" target="_blank" style="color:#d5d5d5;">github.com/hire-me-asap</a> ·
                <a href="#" style="color:#d5d5d5;">Privacy Policy</a>
                </div>
            """)
    


    """ 이벤트 """

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
    

    # chatbot example 함수 및 이벤트   
    def handle_example_click(evt: gr.SelectData):
        """ 이 함수에는 evt 외의 추가 인수를 넣을 수 없음 """
        """ llm 함수 실행(추가 필요) """        
        selected_message = evt.value['text']    
        example_history = []
        example_history.append({"role": "user", "content": selected_message})    
        result = "좋은 질문이에요! 엣취!🤧 지금 분석 중입니다."
        example_history.append({"role": "assistant", "content": result})       
        
        return example_history, example_history
    
    main_chatbot.example_select(handle_example_click, outputs=[main_chatbot, history_state])


    # chatbot 질문 입력 함수 및 이벤트
    def handle_user_message(user_input, user_check, history_state) :
        """ user_check 처리 함수 필요 """
        history_state.append({"role": "user", "content": user_input})
        bot_response = "좋은 질문이에요! 엣취!🤧 지금 분석 중입니다."
        history_state.append({"role": "assistant", "content": bot_response})
        return history_state, history_state  # chatbot과 history_state 각각에 보내서 저장 


    # 함수 실행 후 user_input 지우는 함수 
    def clear_user_input() :
        return gr.update(value=None)

    user_input.submit(handle_user_message, inputs=[user_input, user_check, history_state], outputs=[main_chatbot, history_state]).then(clear_user_input, None, user_input)


    # logo 클릭시 기본 챗 화면으로 이동 
    def return_home() :
        return gr.update(selected=0), gr.update(label=FEATURES['general'], examples=EXAMPLE_MESSAGES['general'])
    
    top_logo.click(return_home, outputs=[tab_host, main_chatbot])


demo.launch()
