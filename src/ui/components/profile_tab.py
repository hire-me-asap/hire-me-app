import gradio as gr

from src.ui.constants import *


class ProfileTab:
    def __init__(self):
        with gr.Tab('프로필', id=1) as profile_tab:
            gr.Markdown('# 💳 사용자 정보 관리')

            with gr.Row():
                with gr.Column(scale=4):
                    self.username_text = gr.Text(
                        label='사용자 이름',
                        placeholder='사용자 ID가 표시됩니다',
                        interactive=False
                    )
                    self.preferred_job = gr.Text(
                        label='희망 직무',
                        placeholder='희망하는 직무를 입력해보세요'
                    )
                    gr.Button('변경사항 저장하기', variant='primary', elem_classes=['profile-save-button'])

                with gr.Column():
                    self.profile_image = gr.Image(interactive=False, scale=1)

            gr.Markdown()
            gr.Markdown('# 📜 이력서 관리')

            with gr.Group():
                self.user_skill_dropdown = gr.Dropdown(
                    ['기술1', '기술2', '기술3'],
                    label='스킬 셋',
                    multiselect=True
                )
                with gr.Row():
                    self.education_level_dropdown = gr.Dropdown(
                        [
                            '초등학교 졸업', '중학교 졸업', '고등학교 졸업',
                            '검정고시 합격', '학사 학위', '석사 학위', '박사 학위'
                        ],
                        label='최종 학력',
                        multiselect=False,
                        interactive=True
                    )
                    self.major_textbox = gr.Textbox(
                        label='전공',
                        placeholder='전공명을 적으세요'
                    )
                self.additional_educations_textbox = gr.TextArea(
                    label='교육사항',
                    placeholder='지원하고자 하는 직무와 관련하여 이수했던 교육들을 나열해주세요'
                )
                self.user_resume_textbox = gr.TextArea(
                    label='경력사항',
                    placeholder='지원하고자 하는 직무와 관련된 업무 경험 및 활동 경험들을 나열해주세요'
                )
                self.additional_info_textbox = gr.TextArea(
                    label='추가적인 정보',
                    placeholder='엣취가 당신에 대해 이해하기 위해 필요한 추가적인 정보를 자유롭게 적어주세요'
                )

            gr.Button('변경사항 저장하기', variant='primary',elem_classes=['profile-save-button'])
            gr.Markdown()

            with gr.Accordion('⚠️ 위험한 기능', open=False):
                gr.Markdown()

                gr.Markdown(
                    '프로필 페이지에 입력된 이력서를 모두 빈칸으로 되돌립니다. 이 작업은 되돌릴 수 없습니다.')
                self.clear_resume_button = gr.Button('이력서 지우기', elem_classes='red-button')
                gr.Markdown()

                gr.Markdown('사용자의 모든 대화 기록을 지웁니다. 이 작업은 되돌릴 수 없습니다.')
                self.clear_history_button = gr.Button('대화 기록 지우기', elem_classes='red-button')