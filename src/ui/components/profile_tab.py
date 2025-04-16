import gradio as gr

from src.ui.constants import *
from src.ui.events import add_row, generate_user_info_json
from src.logic.resume.resume_logic import *


class ProfileTab:
    def __init__(self):
        with gr.Tab('프로필', id=1) as profile_tab:
            """ 프로필 탭 """
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

            gr.Markdown('# 📜 이력서 관리')
            gr.Markdown("### 🥸 개인 정보")
            with gr.Row():
                real_name = gr.Textbox(label='이름', placeholder='본명을 입력하세요')
            with gr.Row():
                summary = gr.Textbox(label='이력서 요약', placeholder='간단하게 본인을 소개해주세요')

    
            gr.Markdown("### 🛠 기술 스택")
            with gr.Row():
                skill_stack = gr.Dropdown(
                choices=ALL_SKILLS,
                multiselect=True,
                filterable=True,
                label = '본인의 기술 스택을 선택해 주세요'
                )

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
            add_btn_edu = gr.Button("➕ 행 추가")

            gr.Markdown("### 💼 경력사항")
            work_experiences = gr.Dataframe(
                headers=['회사명','근무기간 (YYYY.MM - YYYY.MM)' , '직책', '주요 업무'],
                datatype=['str', 'str', 'str', 'str'],
                value=[["", "", "", ""]],
                col_count=(4, "fixed"),
                interactive=True,
                key="edu_df"
            )
            add_btn_work = gr.Button("➕ 행 추가")
            #add_btn.click(fn=add_row, inputs=work_experiences, outputs=work_experiences)

            gr.Markdown("### 🏅 자격증" )
            certificates = gr.Dataframe(
                headers=['자격증명', '취득일 (YYYY.MM.DD)', '발급기관'],
                datatype=['str', 'str', 'str'],
                value=[["", "", ""]],
                col_count=(3, "fixed"),
                interactive=True,
                wrap=True
            )
            add_btn_cert = gr.Button("➕ 행 추가")
            #add_btn.click(fn=add_row, inputs=certificates, outputs=certificates)
        
            gr.Markdown("### 🏆 수상내역" )
            awards = gr.Dataframe(
                headers=['수상명', '수상일 (YYYY.MM.DD)', '주최기관'],
                datatype=['str', 'str', 'str'],
                value=[["", "", ""]],
                col_count=(3, "fixed"),
                interactive=True,
                wrap=True
            )
            add_btn_awards = gr.Button("➕ 행 추가")
            #add_btn.click(fn=add_row, inputs=awards, outputs=awards)

            gr.Markdown("### 🌍 어학" )
            languages = gr.Dataframe(
                headers=['언어', '시험/레벨', '취득일 (YYYY.MM.DD)'],
                datatype=['str', 'str', 'str'],
                value=[["", "", ""]],
                col_count=(3, "fixed"),
                interactive=True,
                wrap=True
            )
            add_btn_lang = gr.Button("➕ 행 추가")
            #add_btn.click(fn=add_row, inputs=languages, outputs=languages)

        with profile_tab:
                gr.Markdown("### 📄 이력서 PDF로 저장하고 싶으신가요?")
                # 📤 PDF 다운로드 버튼 + 파일 컴포넌트
                generate_resume_button = gr.Button("이력서 PDF 생성하기", variant="primary")
                pdf_file_output = gr.File(label="📎 생성된 이력서 PDF")

                # ✅✅✅  변경사항 저장하기 (이력서 DB 업데이트) (update_resume_info)
                save_button = gr.Button("변경사항 저장하기", variant="primary")


                with gr.Accordion('⚠️ 위험한 기능', open=False):
                    gr.Markdown()
                    
                    gr.Markdown('프로필 페이지에 입력된 이력서를 모두 빈칸으로 되돌립니다. 이 작업은 되돌릴 수 없습니다.')                
                    clear_resume_button = gr.Button('이력서 지우기', variant='stop')
                    gr.Markdown()

                    gr.Markdown('사용자의 모든 대화 기록을 지웁니다. 이 작업은 되돌릴 수 없습니다.')
                    clear_history_button = gr.Button('대화 기록 지우기', variant='stop')
                
                resume_info_temp = gr.Textbox(visible=False)
                    

    
    def init_event_handlers(self, app_logic):
    # 기존 인스턴스(app_logic)를 사용하여 원래 함수 호출
        # add 버튼 정의
        self.add_btn_edu.click(fn=add_row, inputs= self.education_and_exp, outputs= self.education_and_exp)
        self.add_btn_work.click(fn=add_row, inputs=self.work_experiences, outputs=self.work_experiences)
        self.add_btn_cert.click(fn=add_row, inputs=self.certificates, outputs=self.certificates)
        self.add_btn_awards.click(fn=add_row, inputs=self.awards, outputs=self.awards)
        self.add_btn_lang.click(fn=add_row, inputs=self.languages, outputs=self.languages)

        
    #app_logic.update_resume_info(**resume_fields)

    #add_btn.click(fn=add_row, inputs=education_and_exp, outputs=education_and_exp)
        self.save_button.click(
            fn= generate_user_info_json,
                    # 딕셔너리 형태로 인자 전달
                    inputs=[
                        self.real_name, self.summary, self.skill_stack, self.final_degree, self.major, self.school_name, self.gpa, self.egree_date,
                        self.education_and_exp, self.work_experiences, self.certificates, self.awards, self.languages
                    ],
                    outputs= self.resume_info_temp
                ).then(
                    fn=ResumeLogic.update_resume_info,
                    inputs= self.resume_info_temp,
                    outputs=None
                )
