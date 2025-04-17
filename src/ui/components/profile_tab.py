import gradio as gr
import tempfile

from pathlib import Path
from src.ui.constants import *
from src.ui.events import add_row, generate_user_info_json_korean, json_to_user_component, clear_history, id_card_update
from src.logic.app_logic import app_logic



class ProfileTab:
    def __init__(self):
        with gr.Tab('프로필', id=1) as profile_tab:
            """ 프로필 탭 """
            with gr.Row():
                with gr.Column(scale=4):
                    self.userid_text = gr.Text(
                        label='사용자 ID', 
                        value=''
                    )
                    self.wanted_job = gr.Text(
                        label='희망 직무', 
                        placeholder='희망하는 직무를 입력해보세요'
                    )
                    self.user_info_save_btn = gr.Button('변경사항 저장하기', variant='primary', elem_classes=['profile-save-button'])

                with gr.Column():
                    self.profile_image = gr.HTML("<img id='user_profile_card' src=''>")

            gr.Markdown('# 📜 이력서 관리')
            gr.Markdown("### 🥸 개인 정보")
            with gr.Row():
                self.real_name = gr.Textbox(label='이름', placeholder='본명을 입력하세요')
            with gr.Row():
                self.summary = gr.Textbox(label='이력서 요약', placeholder='간단하게 본인을 소개해주세요')

    
            gr.Markdown("### 🛠 기술 스택")
            with gr.Row():
                self.skill_stack = gr.Dropdown(
                choices=ALL_SKILLS,
                multiselect=True,
                filterable=True,
                label = '본인의 기술 스택을 선택해 주세요'
                )

            gr.Markdown("### 🎓 학력 정보")
            with gr.Row():
                self.final_degree = gr.Dropdown(
                    ['초등학교 졸업', '중학교 졸업', '고등학교 졸업', '검정고시 합격', '학사 학위', '석사 학위', '박사 학위'],
                    label='최종 학력'
                )
                self.major = gr.Textbox(label='전공', placeholder='전공명을 입력하세요')

            with gr.Row():
                self.school_name = gr.Textbox(label='학교명')
                self.gpa = gr.Textbox(label='학점', placeholder='예: 4.0 / 4.3')

            self.degree_date = gr.Textbox(label='입학-졸업 YYYY.MM', placeholder='YYYY.MM - YYYY.MM')
        
        
            gr.Markdown("### 📘 교육 및 기타 경험")
            self.education_and_exp = gr.Dataframe(
                type="pandas",
                headers=['교육명', '기간 (YYYY.MM - YYYY.MM)'],
                datatype=['str', 'str'],
                value=[["", ""]], 
                row_count='dynamic',              # ✅ 직접 빈 행 초기화
                col_count=(2, "fixed"),
                interactive=True,                  
                key="edu_df"
                )
            self.add_btn_edu = gr.Button("➕ 행 추가")

            gr.Markdown("### 💼 경력사항")
            self.work_experiences = gr.Dataframe(
                type="pandas",
                headers=['회사명','근무기간 (YYYY.MM - YYYY.MM)' , '직책', '주요 업무'],
                datatype=['str', 'str', 'str', 'str'],
                value=[["", "", "", ""]],
                col_count=(4, "fixed"),
                interactive=True,
                key="edu_df"
            )
            self.add_btn_work = gr.Button("➕ 행 추가")
            #add_btn.click(fn=add_row, inputs=work_experiences, outputs=work_experiences)

            gr.Markdown("### 🏅 자격증" )
            self.certificates = gr.Dataframe(
                type="pandas",
                headers=['자격증명', '취득일 (YYYY.MM.DD)'],
                datatype=['str', 'str'],
                value=[["", ""]],
                col_count=(2, "fixed"),
                interactive=True,
                wrap=True
            )
            self.add_btn_cert = gr.Button("➕ 행 추가")
            #add_btn.click(fn=add_row, inputs=certificates, outputs=certificates)
        
            gr.Markdown("### 🏆 수상내역" )
            self.awards = gr.Dataframe(
                type="pandas",
                headers=['수상명', '수상일 (YYYY.MM.DD)'],
                datatype=['str', 'str'],
                value=[["", ""]],
                col_count=(2, "fixed"),
                interactive=True,
                wrap=True
            )
            self.add_btn_awards = gr.Button("➕ 행 추가")
            #add_btn.click(fn=add_row, inputs=awards, outputs=awards)

            gr.Markdown("### 🌍 어학" )
            self.languages = gr.Dataframe(
                type="pandas",
                headers=['어학시험/점수', '취득일 (YYYY.MM.DD)'],
                datatype=['str', 'str'],
                value=[["", ""]],
                col_count=(2, "fixed"),
                interactive=True,
                wrap=True
            )
            self.add_btn_lang = gr.Button("➕ 행 추가")
            #add_btn.click(fn=add_row, inputs=languages, outputs=languages)

        with profile_tab:
                gr.Markdown("### 📄 이력서 PDF로 저장하고 싶으신가요?")
                # 📤 PDF 다운로드 버튼 + 파일 컴포넌트
                self.generate_resume_button = gr.Button("이력서 PDF 생성하기", variant="primary")
                self.pdf_file_output = gr.File(label="📎 생성된 이력서 PDF")

                # ✅✅✅  변경사항 저장하기 (이력서 DB 업데이트) (update_resume_info)
                self.save_button = gr.Button("변경사항 저장하기", variant="primary")


                with gr.Accordion('⚠️ 위험한 기능', open=False):
                    gr.Markdown()
                    
                    gr.Markdown('프로필 페이지에 입력된 이력서를 모두 빈칸으로 되돌립니다. 이 작업은 되돌릴 수 없습니다.')                
                    self.clear_resume_button = gr.Button('이력서 지우기', elem_classes='red-button')
                    gr.Markdown()

                    gr.Markdown('사용자의 모든 대화 기록을 지웁니다. 이 작업은 되돌릴 수 없습니다.')
                    self.clear_history_button = gr.Button('대화 기록 지우기', elem_classes='red-button')
                
                self.resume_info_temp = gr.State({})
                self.user_input_components = gr.State({})

    def init_event_handlers(self, chat_state, real_name, summary, skill_stack, final_degree, major, school_name, gpa, 
                     degree_date, education_exp, work_experiences, cerificates, awards, languages, main_chatbot, sidebarprofile):
        # 기존 인스턴스(app_logic)를 사용하여 원래 함수 호출
        # 각 입력칸 별로 add 버튼 정의
        self.add_btn_edu.click(fn=add_row, inputs= self.education_and_exp, outputs= self.education_and_exp)
        self.add_btn_work.click(fn=add_row, inputs=self.work_experiences, outputs=self.work_experiences)
        self.add_btn_cert.click(fn=add_row, inputs=self.certificates, outputs=self.certificates)
        self.add_btn_awards.click(fn=add_row, inputs=self.awards, outputs=self.awards)
        self.add_btn_lang.click(fn=add_row, inputs=self.languages, outputs=self.languages)

        # 유저 인포 저장 버튼 -> 새 프로필 카드 생성 -> 프로필탭, 사이드바 이미지 새로고침  
        self.user_info_save_btn.click(app_logic.update_user_wanted, inputs=self.wanted_job).then(id_card_update, outputs=[self.profile_image, sidebarprofile])

        # 이력서 저장 버튼 -> db에 저장 -> db 내용 불러오기 -> 불러온 내용 화면에 출력 (새로고침과 비슷한 효과)
        self.save_button.click(
            fn=generate_user_info_json_korean,
                    # 딕셔너리 형태로 인자 전달
                    inputs=[
                        self.real_name, self.summary, self.skill_stack, self.final_degree, self.major, self.school_name, self.gpa, self.degree_date,
                        self.education_and_exp, self.work_experiences, self.certificates, self.awards, self.languages
                    ],
                    outputs= self.resume_info_temp
                ).then(
                    fn=app_logic.update_resume_info,
                    inputs= self.resume_info_temp,
                    outputs=None
                ).then(app_logic.get_resume_info, outputs=[self.user_input_components]
                ).then(json_to_user_component, inputs=[self.user_input_components], 
                        outputs=[real_name, summary, skill_stack, final_degree, major, school_name, gpa, 
                        degree_date, education_exp, work_experiences, cerificates, awards, languages])

        # 이력서 생성(pdf) 버튼 -> static 폴더에 저장된 파일을 출력  
        self.generate_resume_button.click(
            fn=app_logic.generate_resume_pdf,
            inputs=[],  # 입력 없음! (user_id는 내부적으로 self._user_id로 처리되니까)
            outputs=self.pdf_file_output  # 파일 컴포넌트로 연결
        )

        # (red) 이력서 내용 전부 지우기 버튼 -> db 클리어 -> db 내용 불러오기 -> 불러온 내용 화면에 출력 (새로고침과 비슷한 효과)
        self.clear_resume_button.click(app_logic.reset_resume_info).then(app_logic.get_resume_info, outputs=[self.user_input_components]
                ).then(json_to_user_component, inputs=[self.user_input_components], 
                        outputs=[real_name, summary, skill_stack, final_degree, major, school_name, gpa, 
                        degree_date, education_exp, work_experiences, cerificates, awards, languages])
        
        # (red) chatbot 내용 지우기 버튼 
        self.clear_history_button.click(app_logic.delete_update_user_thread_id).then(clear_history, outputs=[main_chatbot, chat_state])