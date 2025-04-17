import gradio as gr

# 초기 대화 히스토리 설정
history = [
    {"role": "assistant", "content": "어서오세요! Hire Me ASAP 입니다.\n취업 분석을 원하시면 이력서를 업로드 해보세요.😀"},
    {"role": "user", "content": "안녕 나는 평생 직장을 찾고 있어"}
]

# Gradio 테마 설정
theme = gr.themes.Soft(
    primary_hue="gray",
    secondary_hue="stone",
    neutral_hue="zinc",
    font=[
        gr.themes.GoogleFont('Noto Sans Korean'),
        gr.themes.GoogleFont('42dot Sans'),
        gr.themes.GoogleFont('Nanum Gothic'),
        'sans-serif'
    ]
).set(button_transform_hover='*button_primary_background_fill', checkbox_label_shadow='none', checkbox_label_text_size='text_sm')

# 커스텀 CSS 정의 - 너무 길어서 css 파일로 따로 저장 
with open("style.css", "r", encoding='utf-8') as f:
    custom_css = f.read()  # gradio는 str 타입만 넣을 수 있으므로 read() 해서 넣어야 함 


# Gradio 앱 구성
with gr.Blocks(theme=theme, css=custom_css) as demo:
    chat_history = gr.State([])  ## history state에 저장 
    
    # 로그인 기능 = 구현 필요 (도은)
    def log_in() :
        return gr.update(visible=False), gr.update(visible=False), gr.update(visible=True), gr.update(visible=True)
    
    # gradio 기본기능인 exmaple 기능 사용, 이 함수에는 evt 외의 추가 인수를 넣을 수 없음     
    def handle_example_click(evt: gr.SelectData):
        """ llm 함수 실행 """
        result = "좋은 질문이에요! 엣취!🤧 지금 분석 중입니다."
        example_history = [{"role": "user", "content": evt.value['text']}, {"role": "assistant", "content": result}]
        return example_history
    
    ### multimodal용 함수 처리 
    def handle_user_message(user_msg, history) :
        # 파일이 한개인 경우 
        input_file = user_msg['files']
        history.append({"role": "user", "content": {"path": input_file}})   # llm에서 요구하는 대로 작성(수정 필요)
        # 파일이 여러개인 경우 
        # for file in user_msg['files'] :
        #     history.append({"role": "user", "content": {"path": file}})
        text = user_msg['text']
        history.append({"role": "user", "content": text})
        response = ""    ## llm 넣어서 response 받음 
        imsi_response = "좋은 질문이에요! 엣취!🤧 지금 분석 중입니다."
        history.append({"role": "assistant", "content": imsi_response})
        return history, history
    
    # ### 기존 사용자 입력 처리 함수
    # def handle_user_message(user_msg, chat_history):     
    #     chat_history = chat_history or []
    #     chat_history.append({"role": "user", "content": user_msg})
    #     assistant_response = "좋은 질문이에요! 엣취!🤧 지금 분석 중입니다."
    #     chat_history.append({"role": "assistant", "content": assistant_response})
    #     return chat_history, chat_history  # 하나는 Chatbot용, 하나는 State용
    
    # 사용자 텍스트 지우는 함수 
    def clear_user_input() :
        return gr.update(value=None)
    
    # 엣취 로고
    with gr.Row(elem_id="logo-container"):
        gr.Image(
            value="logo_diagonal.png",
            show_label=False,
            container=False,
            show_download_button=False,
            show_share_button=False,
            show_fullscreen_button=False
        )

    examples = [{"text" : "강남 AI 엔지니어 채용 공고 찾아줘"}, 
    {"text" : "파이썬 혼자 공부하려는데, 좋은 강의 있을까?"}, 
    {"text" : "AI 쪽으로 커리어 타려면 뭐부터 해야 돼?"}, 
    {"text" : "프롬프트 엔지니어는 무슨 일을 해?"}]


    # 챗봇 영역
    chatbot = gr.Chatbot(
        height="75vh",
        type='messages',
        container=False,
        avatar_images=("chicken.png", "logo.jpeg"),
        elem_classes="chatbot-box",
        examples=examples
    )

    # 사이드바
    with gr.Sidebar(open=False):
        with gr.Column(elem_classes='sidebar-column') :
            # 로그인 버튼 그룹 / 로그인 시 프로필로 전환 
            with gr.Row(elem_classes="login-group") :
                sign_up_sso = gr.Button("Sign up", visible=True, size="sm", scale=1, elem_classes="login-button")
                login_sso = gr.Button("Log In", visible=True, size="sm", scale=1, elem_classes="login-button")
            profile = gr.Markdown("👤 프로필", visible=False)
            profile_img = gr.Image(value="profile_card.png", width="240px", show_label=False, show_download_button=False, show_fullscreen_button=False, show_share_button=False, elem_classes=["profile-img"], visible=False)
            
            gr.Markdown("🔮 나만을 위한 커리어 길라잡이")

            # 김진솔 수정 0410: 순서 바꿈 (다시)
            # 버튼 개별화 : for문으로 압축해보려 했는데, 압축시 동적함수 생성 필요 -> gradio 자체에서 막혀있음, 우회 필요 -> 그냥 간단하게 개별로 리스너 연결하기로 함
            btn_job = gr.Button("🎯 나에게 맞는 직무는?", value="나에게 맞는 직무를 추천해줘", size="sm")
            btn_roadmap = gr.Button("📍 커리어 로드맵 그리기", value="나에게 맞는 커리어 로드맵을 만들어줘", size="sm")
            btn_company = gr.Button("🔍 인생 회사 찾기", value="나에게 맞는 공고를 추천해줘", size="sm")
            btn_weakness = gr.Button("🔥 내가 보완할 부분은?", value="채용 공고들과 커리어로드맵을 고려할 때 내가 보완해야할 부분은 뭘까?", size="sm")
            
            btn_save_chat = gr.DownloadButton("📂 대화 내용 저장하기", value="filepath", variant="huggingface", size="sm")

            # 빈 공간
            
                    
            # about_us 이미지
            with gr.Column(elem_classes='about-us'):
                with gr.Group(elem_classes=["about-us img"]):
                    gr.Image(
                        value="AboutUS.png",
                        show_label=False,
                        container=False,
                        show_download_button=False,
                        show_share_button=False,
                        show_fullscreen_button=False
                    )

    ## 신규 입력 - 깔끔 버전
    with gr.Column() :
        user_input = gr.MultimodalTextbox(placeholder="이력서를 첨부하거나 질문을 해주세요", show_label=False)
        user_checked = gr.CheckboxGroup(choices=["관련 강의 추천 받기", "이력서 포함하여 답변 받기"], container=False, elem_classes=["custom-checkbox"])


    #### 기존 입력 
    # # 사용자 입력창, 업로드, 체크박스, 발송 버튼, 하단 저작권
    # with gr.Row(elem_classes=["checkbox-row"]):
    #     gr.UploadButton(label="upload", icon="img.png", file_types=["image"], scale=1, elem_classes=["custom-button"])
    #     with gr.Column(elem_classes=["custom-input"], scale=30):
    #         user_input = gr.Textbox(placeholder="무엇이든 물어보세요", show_label=False, scale=30)
    #         with gr.Row():  # ✅ 체크박스 2개를 같은 줄에 배치
    #             chk_recommend = gr.Checkbox(label="🪄 관련 강의 추천 받기", elem_classes=["custom-checkbox"])
    #             chk_resume = gr.Checkbox(label="📑 이력서 포함하여 답변 받기", elem_classes=["custom-checkbox"])
    #     submit_btn = gr.Button("🚀", scale=1, size="lg", elem_classes=["custom-button"])
    
    # 고권아 추가 0410
    # 사이트 하단 푸터
    gr.Markdown("""
        <div class="site-footer">
                © 2025 hire me ASAP Inc. ·
                ✉️ contact@hiremeasap.com ·
                <a href="https://github.com/hire-me-asap" target="_blank" style="color:#d5d5d5;">github.com/hire-me-asap</a> ·
                <a href="#" style="color:#d5d5d5;">Privacy Policy</a>
                </div>
            """)

            
    # example 클릭시 chatbot 시작
    chatbot.example_select(handle_example_click, outputs=[chatbot])

    # 로그인 버튼 클릭시 프로필 보여주기
    login_sso.click(log_in, outputs=[sign_up_sso, login_sso, profile, profile_img])

    # 사용자 질문 제출 처리
    user_input.submit(fn=handle_user_message, inputs=[user_input, chatbot], outputs=[chatbot, chat_history]).then(clear_user_input, None, user_input)
    
    # 사이드바 버튼 클릭시 처리 
    btn_job.click(handle_user_message, inputs=[btn_job, chat_history], outputs=[chatbot, chat_history])
    btn_roadmap.click(handle_user_message, inputs=[btn_roadmap, chat_history], outputs=[chatbot, chat_history])
    btn_company.click(handle_user_message, inputs=[btn_company, chat_history], outputs=[chatbot, chat_history])
    btn_weakness.click(handle_user_message, inputs=[btn_weakness, chat_history], outputs=[chatbot, chat_history])
