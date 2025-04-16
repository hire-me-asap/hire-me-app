import gradio as gr

from src.ui.constants import *


class ProfileTab:
    def __init__(self):
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

        with profile_tab:
                gr.Markdown("### 📄 이력서 PDF로 저장하고 싶으신가요?")
                # 📤 PDF 다운로드 버튼 + 파일 컴포넌트
                generate_resume_button = gr.Button("이력서 PDF 생성하기", variant="primary")
                pdf_file_output = gr.File(label="📎 생성된 이력서 PDF")

                # 변경사항 저장하기 (이력서 DB 업데이트)
                save_button = gr.Button("변경사항 저장하기", variant="primary")

               
                save_button.click(
                    fn=call_update_resume_info,
                    inputs=[
                        real_name, summary, skill_stack, final_degree, major, school_name, gpa, degree_date,
                        education_and_exp, work_experiences, certificates, awards, languages
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


"""함수"""

"""            # 행 추가 버튼 클릭 시 DataFrame에 빈 행 추가
def add_row(df):
                if isinstance(df, pd.DataFrame):
                    new_row = pd.DataFrame([[ "" for _ in df.columns ]], columns=df.columns)
                    return pd.concat([df, new_row], ignore_index=True)
                else:
                    # 초기 리스트 형태일 경우에도 유연하게 처리
                    df.append(["" for _ in df[0]])
                    return df
 def remap_dataframe(df, keymap):
                    if isinstance(df, pd.DataFrame):
                        return [
                                {keymap.get(k, k): v for k, v in row.items()}
                                for _, row in df.iterrows()
                            ]
                    else:
                        return []
                    
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
                    }

                    return user_info_json  # 이 반환값은 이후 DB 저장 로직이나 PDF 생성으로 전달
def call_update_resume_info(
    real_name, summary, skill_stack, final_degree, major, school_name, gpa, degree_date,
    education_and_exp, work_experiences, certificates, awards, languages
):
    resume_fields = {
        'real_name': real_name,
        'summary': summary,
        'skill_stack': skill_stack,
        'education': [{
            'school_name': school_name,
            'degree_date': degree_date,
            'final_degree': final_degree,
            'major': major,
            'gpa': gpa
        }],
        'education_and_exp': df_to_list(education_and_exp),
        'work_experiences': df_to_list(work_experiences),
        'certificates': df_to_list(certificates),
        'awards': df_to_list(awards),
        'languages': df_to_list(languages),
    }

    # 기존 인스턴스(app_logic)를 사용하여 원래 함수 호출
    app_logic.update_resume_info(**resume_fields)
"""