import gradio as gr

with gr.Blocks(css_paths=['src/tmp/ui-test-style.css']) as demo:
    """ 앱 """

    with gr.Sidebar(position='left') as sidebar:
        """ 사이드바 """

        sidebar_logo_image = gr.Image(
            './resources/logo_diagonal.png',
            elem_id='sidebar-logo',
            elem_classes=['click_to_home'],
            show_label=False,
            container=False,
            show_download_button=False,
            show_share_button=False,
            show_fullscreen_button=False,
        )

        general_chat_button = gr.Button('무엇이든 물어보세요!')

        profile_button = gr.Button('이력서 입력하러 가기', variant='primary')

        with gr.Group():
            gr.HTML('📊 <b>맞춤 직무 설계<b>')
            job_chat_button = gr.Button('직무 찾기')
            recruit_chat_button = gr.Button('채용 공고 찾기')
            resume_chat_button = gr.Button('이력서 검토하기')
            roadmap_chat_button = gr.Button('취업 준비 로드맵 작성하기')

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
            './resources/logo_diagonal.png',
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
                    type='messages',
                    examples=[
                        {'role': 'assistant', 'text': '예시 1'},
                        {'role': 'assistant', 'text': '예시 2'},
                        {'role': 'assistant', 'text': '예시 3'},
                        {'role': 'assistant', 'text': '예시 4'},
                    ],
                    show_label=False
                )
                gr.TextArea(lines=1, max_lines=5,
                            submit_btn=True, show_label=False)
                gr.HTML('엣취는 실수를 할 수 있습니다.')

        with gr.Tab('프로필', id=1) as profile_tab:
            """ 프로필 탭 """

            gr.Markdown('### 사용자 정보 관리')

            with gr.Row():
                with gr.Column(scale=4):
                    username_text = gr.Text(
                        label='사용자 이름', placeholder='사용자 ID가 표시됩니다', interactive=False)
                    preferred_job = gr.Text(
                        label='희망 직무', placeholder='희망하는 직무를 입력해보세요')

                with gr.Column():
                    profile_image = gr.Image(interactive=False, scale=1)

            gr.Markdown('### 이력서 관리')

            with gr.Group():
                user_skill_dropdown = gr.Dropdown(
                    ['기술1', '기술2', '기술3'], label='스킬 셋', multiselect=True)
                with gr.Row():
                    education_level_dropdown = gr.Dropdown(
                        ['중학교 졸업', '고등학교 졸업', '대학교 학사 학위'], label='최종 학력', multiselect=False, interactive=True)
                    major_textbox = gr.Textbox(
                        label='전공', placeholder='전공명을 적으세요')
                additional_educations_textbox = gr.TextArea(
                    label='그 밖의 교육', placeholder='이수했던 교육을 추가로 설명해보세요')
                user_resume_textbox = gr.TextArea(
                    label='이력서', placeholder='직무 관련 경험을 입력해주세요')
                user_resume_textbox = gr.TextArea(
                    label='이력서', placeholder='직무 관련 경험을 입력해주세요')

            gr.Button('변경사항 저장하기', variant='primary')

            with gr.Accordion('⚠️ 위험한 기능', open=False):
                clear_history_button = gr.Button(
                    '모든 사용 기록 지우기', variant='stop')
                clear_history_button = gr.Button(
                    '모든 사용 기록 지우기', variant='stop')
                clear_history_button = gr.Button(
                    '모든 사용 기록 지우기', variant='stop')
                clear_history_button = gr.Button(
                    '모든 사용 기록 지우기', variant='stop')
                clear_history_button = gr.Button(
                    '모든 사용 기록 지우기', variant='stop')
                clear_history_button = gr.Button(
                    '모든 사용 기록 지우기', variant='stop')
                clear_history_button = gr.Button(
                    '모든 사용 기록 지우기', variant='stop')
                clear_history_button = gr.Button(
                    '모든 사용 기록 지우기', variant='stop')

    """ 이벤트 """
    
    def set_topbar_visibility(is_visible):
        return gr.update(visible=is_visible)
    
    sidebar.expand(lambda: set_topbar_visibility(False), outputs=[topbar])
    sidebar.collapse(lambda: set_topbar_visibility(True), outputs=[topbar])
    
    def select_profile_tab():
        return gr.update(selected=1)
    
    profile_button.click(lambda: select_profile_tab(), outputs=[tab_host])
    
    def select_chat_tab(mode=None):
        # IMPL: 사용자가 선택한 모드에 따라 적절한 기능 구현
        
        return gr.update(selected=0)
    
    general_chat_button.click(lambda: select_chat_tab(), outputs=[tab_host])
    job_chat_button.click(lambda: select_chat_tab(), outputs=[tab_host])
    recruit_chat_button.click(lambda: select_chat_tab(), outputs=[tab_host])
    resume_chat_button.click(lambda: select_chat_tab(), outputs=[tab_host])
    roadmap_chat_button.click(lambda: select_chat_tab(), outputs=[tab_host])
    

demo.launch(debug=True)
