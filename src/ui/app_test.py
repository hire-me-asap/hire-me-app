
import gradio as gr
import base64
import os
import sys
import pandas as pd

from dotenv import load_dotenv
from ..logic.app_logic import app_logic

load_dotenv()

from openai import AzureOpenAI

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

# 원티드 전체 기술스택 리스트 (80개 중 일부 예시)
# 원티드 전체 기술스택 리스트 (내림차순 89개)
ALL_SKILLS = [
    "Python", "AWS", "Git", "JavaScript", "React", "TypeScript", "Java",
    "Docker", "MySQL", "GitHub", "Linux", "C++", "Kubernetes", "Spring Framework",
    "Kotlin", "Node.js", "SQL", "PyTorch", "Spring Boot", "Next.js", "C",
    "HTML", "C / C++", "PostgreSQL", "iOS", "Redis", "Django", "React Native",
    "Android", "Nest.js", "React.js", "JIRA", "MongoDB", "Go", "Tensorflow",
    "Notion", "JPA", "Restful API", "Slack", "Flutter", "C#", "Vue.js",
    "Swift", "FastAPI", "GCP", "RDBMS", "NoSQL", "CSS", "Rust", "PHP",
    "Oracle", "Golang", "Azure", "Jenkins", "GraphQL", "CUDA", "ElasticSearch",
    "ML", "Figma", "GitLab", "OpenCV", "Flask", "Spark", "Confluence",
    "HTML5", "DevOps", "Terraform", "ExpressJS", "QA 엔지니어링", "API",
    "jQuery", "Angular", "딥 러닝", "ROS", "Ubuntu", "펌웨어", "Scikit-Learn",
    "Hadoop", "Redux", "Scala", "NLP", "NumPy", "Nginx", "ORCAD", "SASS",
    "FPGA", "VueJS", "MS 오피스", "Qt"
]

# gradio_0413_style-basic
# theme = gr.themes.Soft(
#     primary_hue="slate",
#     secondary_hue="stone",
#     neutral_hue="zinc",
    
# ).set(
#     button_large_text_weight=400,
#     block_title_text_weight=400,
# )
"""
이력서 관련 함수들
"""

def handle_save_resume(
        real_name,                 # 사용자 이름: str
        summary,                   # 사용자 요약: str
        skill_stack,               # 기술 스택: List[str]
        final_degree,              # 최종 학력: str
        major,                     # 전공: str
        school_name,               # 학교명: str
        gpa,                       # 학점: str or float
        degree_date,               # 입학-졸업 기간: str ("YYYY.MM - YYYY.MM")
        education_and_exp,         # 교육 및 기타 경험: gr.Dataframe
        work_experiences,          # 경력 사항: gr.Dataframe
        certificates,              # 자격증: gr.Dataframe
        awards,                    # 수상 내역: gr.Dataframe
        languages,                 # 외국어: gr.Dataframe
        additional_info            # 추가 정보: str
    ):
        # 학력 항목은 단일 입력이지만 서버로 보낼 때는 리스트 형태로 래핑 (DB 일관성 유지 목적)
        education = [{
            "school_name": school_name,         # 예: "서울대학교"
            "degree_date": degree_date,         # 예: "2019.03 - 2023.02"
            "final_degree": final_degree,       # 예: "학사"
            "major": major,                     # 예: "경영정보학"
            "gpa": gpa                          # 예: "4.1"
        }]

        # 전체 user_info 구조를 JSON(dict) 형태로 조립
        user_info = {
            "real_name": real_name,                           # 사용자 이름
            "summary": summary,                               # 사용자 요약
            "skill_stack": skill_stack,                             # 예: ["Python", "SQL"]
            "education": education,                     # 단일 학력 → 리스트
            "education_and_exp": df_to_list(education_and_exp),     # 교육 & 기타 경험 → JSON 리스트
            "work_experiences": df_to_list(work_experiences),       # 경력사항
            "certificates": df_to_list(certificates),               # 자격증
            "awards": df_to_list(awards),                           # 수상내역
            "languages": df_to_list(languages),                     # 외국어
            "additional_info": additional_info                      # 기타 소개글
        }

        # 확인용 출력 (개발 중 디버깅 또는 프린트 용도)
        print("[✅ 저장된 user_info JSON]", user_info)

def generate_user_info_json(
    real_name, summary, skill_stack, final_degree, major, school_name, gpa, degree_date, education_and_exp_df, work_experiences_df,
    certificates_df, awards_df, languages_df,
    additional_info
):

    # ✅ 그라디오 헤더 → 실제 저장 키 이름 매핑
    education_and_exp_keymap = {
        "교육명": "edu_exp",
        "기간 (YYYY.MM - YYYY.MM)": "edu_exp_date"
    }
    work_experiences_keymap = {
        "회사명": "company",
        "근무기간 (YYYY.MM - YYYY.MM)": "work_date",
        "직책": "position",
        "주요 업무": "work_description"
    }
    certificates_keymap = {
        "자격증명": "certificate",
        "취득일 (YYYY.MM.DD)": "certificate_date",
        "발급기관": "certificate_org"
    }
    awards_keymap = {
        "수상명": "award",
        "수상일 (YYYY.MM.DD)": "award_date",
        "주최기관": "award_org"
    }
    languages_keymap = {
        "언어": "language",
        "시험/레벨": "language_level",
        "취득일 (YYYY.MM.DD)": "language_date"
    }

    # ✅ keymap에 따라 헤더 변환 함수
    def remap_dataframe(df, keymap):
        if isinstance(df, pd.DataFrame):
            return [
                {keymap.get(k, k): v for k, v in row.items()}
                for _, row in df.iterrows()
            ]
        else:
            return []

    # ✅ education은 단일 항목 리스트로 구성
    education_json = [{
        "school_name": school_name,
        "degree_date": degree_date,
        "final_degree": final_degree,
        "major": major,
        "gpa": gpa
    }]

    # ✅ 전체 JSON 구조 생성
    user_info_json = {
        "real_name": real_name,
        "summary": summary,
        "skill_stack": skill_stack,
        "education": education_json,
        "education_and_exp": remap_dataframe(education_and_exp_df, education_and_exp_keymap),
        "work_experiences": remap_dataframe(work_experiences_df, work_experiences_keymap),
        "certificates": remap_dataframe(certificates_df, certificates_keymap),
        "awards": remap_dataframe(awards_df, awards_keymap),
        "languages": remap_dataframe(languages_df, languages_keymap),
        "additional_info": additional_info
    }

    print("✅ 저장된 user_info JSON")
    import json
    print(json.dumps(user_info_json, indent=2, ensure_ascii=False))

    return user_info_json  # 이 반환값은 이후 DB 저장 로직이나 PDF 생성으로 전달

theme = gr.themes.Citrus(
    primary_hue="slate",
    secondary_hue="rose",
    neutral_hue="zinc",
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



# gr.HTML 에서 로컬 디렉토리 파일을 못불러오기 때문에 따로 불러와줌 
with open("logo.png", "rb") as f:
    image_data = base64.b64encode(f.read()).decode("utf-8")
# 주소 설정 
img_html = f'<img src="data:image/png;base64,{image_data}">'

""" css 목록
 gradio_0413_style-basic.css
 gradio_0413_style-citrus.css
 gradio_0413_style-????.css
 """ 

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

            with gr.Group():
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

            gr.Markdown('# 📜 이력서 관리')
            with gr.Group(): 
                gr.Markdown("### 🥸 개인 정보")
                with gr.Row():
                    real_name = gr.Textbox(label='이름', placeholder='본명을 입력하세요')
                with gr.Row():
                    summary = gr.Textbox(label='이력서 요약', placeholder='간단하게 본인을 소개해주세요')

            with gr.Group():
                gr.Markdown("### 🛠 기술 스택")
                with gr.Row():
                    skill_stack = gr.Dropdown(
                    choices=ALL_SKILLS,
                    multiselect=True,
                    filterable=True,
                    label = '본인의 기술 스택을 선택해 주세요'
                    )

            with gr.Group(): 
                gr.Markdown("### 🎓 학력 정보")
                with gr.Row():
                    final_degree = gr.Dropdown(
                        ['초등학교 졸업', '중학교 졸업', '고등학교 졸업', '검정고시 합격', '학사 학위', '석사 학위', '박사 학위'],
                        label='최종 학력'
                    )
                    major = gr.Textbox(label='전공', placeholder='전공명을 입력하세요')

                with gr.Row():
                    school_name = gr.Textbox(label='학교명')
                    gpa = gr.Textbox(label='학점', placeholder='예: 4.0 / 4.3')

                degree_date = gr.Textbox(label='입학-졸업 YYYY.MM', placeholder='YYYY.MM - YYYY.MM')

            # 행 추가 버튼 클릭 시 DataFrame에 빈 행 추가
            def add_row(df):
                if isinstance(df, pd.DataFrame):
                    new_row = pd.DataFrame([[ "" for _ in df.columns ]], columns=df.columns)
                    return pd.concat([df, new_row], ignore_index=True)
                else:
                    # 초기 리스트 형태일 경우에도 유연하게 처리
                    df.append(["" for _ in df[0]])
                    return df
            
            with gr.Group(): 
                gr.Markdown("### 📘 교육 및 기타 경험")
                education_and_exp = gr.Dataframe(
                        headers=['교육명', '기간 (YYYY.MM - YYYY.MM)'],
                        datatype=['str', 'str'],
                        value=[["", ""]], 
                        row_count='dynamic',              # ✅ 직접 빈 행 초기화
                        col_count=(2, "fixed"),
                        interactive=True,                  
                        key="edu_df"
                    )
                add_btn = gr.Button("➕ 행 추가")
                add_btn.click(fn=add_row, inputs=education_and_exp, outputs=education_and_exp)
            with gr.Group():     
                gr.Markdown("### 💼 경력사항")
                work_experiences = gr.Dataframe(
                    headers=['회사명','근무기간 (YYYY.MM - YYYY.MM)' , '직책', '주요 업무'],
                    datatype=['str', 'str', 'str', 'str'],
                    value=[["", "", "", ""]],
                    interactive=True,
                    key="edu_df"
                )
                add_btn = gr.Button("➕ 행 추가")
                add_btn.click(fn=add_row, inputs=work_experiences, outputs=work_experiences)
            with gr.Group():     
                gr.Markdown("### 🏅 자격증" )
                certificates = gr.Dataframe(
                    headers=['자격증명', '취득일 (YYYY.MM.DD)', '발급기관'],
                    datatype=['str', 'str', 'str'],
                    value=[["", "", ""]],
                    interactive=True,
                    wrap=True
                )
                add_btn = gr.Button("➕ 행 추가")
                add_btn.click(fn=add_row, inputs=certificates, outputs=certificates)
            
            with gr.Group():   
                gr.Markdown("### 🏆 수상내역" )
                awards = gr.Dataframe(
                    headers=['수상명', '수상일 (YYYY.MM.DD)', '주최기관'],
                    datatype=['str', 'str', 'str'],
                    value=[["", "", ""]],
                    interactive=True,
                    wrap=True
                )
                add_btn = gr.Button("➕ 행 추가")
                add_btn.click(fn=add_row, inputs=awards, outputs=awards)

            with gr.Group():   
                gr.Markdown("### 🌍 어학" )
                languages = gr.Dataframe(
                    headers=['언어', '시험/레벨', '취득일 (YYYY.MM.DD)'],
                    datatype=['str', 'str', 'str'],
                    value=[["", "", ""]],
                    interactive=True,
                    wrap=True
                )
                add_btn = gr.Button("➕ 행 추가")
                add_btn.click(fn=add_row, inputs=languages, outputs=languages)

            with gr.Group():   
                gr.Markdown("### 📝 추가 정보" )
                additional_info = gr.TextArea(
                    placeholder='엣취가 당신에 대해 이해하기 위해 필요한 추가적인 정보를 자유롭게 적어주세요'
                )

        with profile_tab:
                gr.Markdown("### 📄 이력서 PDF로 저장하고 싶으신가요?")

                # 📤 PDF 다운로드 버튼 + 파일 컴포넌트
                generate_resume_button = gr.Button("이력서 PDF 생성하기", variant="primary")
                pdf_file_output = gr.File(label="📎 생성된 이력서 PDF")

                
                save_button = gr.Button("변경사항 저장하기", variant="primary")

                save_button.click(
                    fn=app_logic.update_resume_info(), #app_logic.py에 있음
                    inputs=[
                        real_name, summary, skill_stack, final_degree, major, school_name, gpa, degree_date,
                        education_and_exp, work_experiences,
                        certificates, awards, languages,
                        additional_info
                    ],
                    outputs=[]
                )
            
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

            # 기술 스택 실시간 검색 필터링 함수
    def filter_skills(query):
        if not query:
            return []
        return [skill for skill in ALL_SKILLS if query.lower() in skill.lower()]

    # 클릭한 단어를 선택된 skill 리스트에 추가
    def add_to_selected(text, selected):
            if text and text not in selected:
                selected.append(text)
            return gr.update(value=selected)
    
    # ✅ DataFrame → 리스트[딕셔너리]로 변환
    def df_to_list(df):
        if isinstance(df, pd.DataFrame):
            return df.to_dict(orient="records")
        return []
    
demo.launch()