import gradio as gr

with gr.Blocks(css_paths=['src/tmp/ui-test-style.css']) as demo:
    """ 앱 """
    
    with gr.Sidebar(position='left'):
        """ 사이드바 """
        
        sidebar_profile_image = gr.Image(
            './resources/logo_diagonal.png',
            width=40,
            elem_id='logo',
            show_label=False,
            container=False,
            show_download_button=False,
            show_share_button=False,
            show_fullscreen_button=False,
        )
        
        gr.Button('무엇이든 물어보세요!')   
        
        profile_button = gr.Button('이력서 입력하러 가기', variant='primary')
        
        with gr.Group():
            gr.HTML('📊 <b>맞춤 직무 설계<b>')
            job_button = gr.Button('직무 찾기')
            recruit_button = gr.Button('채용 공고 찾기')
            resume_button = gr.Button('이력서 검토하기')
            roadmap_button = gr.Button('취업 준비 로드맵 작성하기')
        
               
        gr.Image(
            './resources/retro_id_card.png',
            elem_id='profile',
            show_label=False,
            container=False,
            show_download_button=False,
            show_share_button=False,
            show_fullscreen_button=False,
        )

    with gr.Tabs():
        """ 탭 호스트 """

        with gr.Tab('엣취', elem_id='chatbot-tab'):
            """ 엣취 탭 """
            
            with gr.Group():
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

        with gr.Tab('프로필'):
            """ 프로필 탭 """   
            
            with gr.Row():
                with gr.Column(scale=4):
                    username_text = gr.Text(label='사용자 이름')
                    with gr.Group():
                        user_skill_ = gr.Dropdown(
                            ['기술1', '기술2', '기술3'], label='스킬 셋', multiselect=True)
                        user_resume_textbox = gr.TextArea(
                            label='이력서', placeholder='직무 관련 경험을 입력해주세요')

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

                with gr.Column():
                    profile_image = gr.Image(interactive=False, scale=1)
                    gr.Button('변경사항 저장하기', variant='primary')


demo.launch(debug=True)
