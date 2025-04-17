import gradio as gr

from src.ui.constants import *
from src.ui.events import select_example, process_user_message, toggle_resume_usage, load_archive_images
from src.logic.app_logic import app_logic


class ChatbotTab:
    def __init__(self):
        with gr.Tab('엣취', id=0, elem_id='chatbot-tab') as chatbot_tab:
            self.main_chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                label=FEATURES[Modes.GENERAL],
                type='messages',
                examples=EXAMPLE_MESSAGES[Modes.GENERAL],
                avatar_images=[
                    "resources/hatching_chick.png",
                    "resources/icon.png",
                ]
            )
            with gr.Group(elem_classes=['user-inputs', 'block', 'svelte-11xb1hd']):
                with gr.Row(elem_classes=['row-vertical-center']):
                    self.user_check = gr.CheckboxGroup(
                        [INCLUDE_RESUME],
                        value=[INCLUDE_RESUME],
                        show_label=False,
                        elem_id="custom-checkbox",
                        interactive=True,
                        container=False
                    )
                    gr.Markdown('엣취는 실수를 할 수 있습니다.', elem_id='etch_kawai')

                self.input_textarea = gr.TextArea(
                    placeholder='❔ 엣취에게 물어보세요',
                    elem_id='user-input-txt',
                    lines=1,
                    max_lines=5,
                    submit_btn=True,
                    show_label=False,
                )

        self.chatbot_tab = chatbot_tab

    def init_event_handlers(self, chat_state, citation_contents, archive_gallery):
        self.main_chatbot.example_select(
            select_example, outputs=[self.input_textarea])

        self.input_textarea.submit(
            process_user_message,
            inputs=[self.input_textarea, chat_state],
            outputs=[self.input_textarea, self.main_chatbot, chat_state],
            scroll_to_output=True,
            queue=True
        ).then(
            load_archive_images,
            inputs=[],
            outputs=[archive_gallery]
        )

        # TODO: 기능 구현 후에 아래 이벤트 핸들러는 제거해주세요.
        def test_select(select_data: gr.SelectData, chat_state):
            history = chat_state['histories'][chat_state['mode']]
            idx = select_data.index

            if idx >= len(history):
                return

            message = history[idx]

            # if 'citations' in message:
            #     print(f'@@@ Citational message: {message["citations"]}')
            # else:
            #     print('@@@ No citations found.')

        def update_citation(select_data: gr.SelectData, chat_state):
            history = chat_state['histories'][chat_state['mode']]
            idx = select_data.index

            if idx >= len(history):
                return

            message = history[idx]

            # print(f'message type : {type(message)}')
            # print(f'keys : {message.keys()}')
            # print(message)
            # message['raw_message'] 는 dict

            if 'raw_message' in message and message['raw_message']:
                # print(message['raw_message'])
                citation_url_list = app_logic.extract_citations_to_url(
                    message['raw_message'])
                # print(citation_url_list)
                if citation_url_list:
                    # Markdown 형식으로 참조 문헌 목록 생성
                    markdown_content = "## 참조 문헌 목록\n\n"
                    for idx, item in enumerate(citation_url_list, 1):
                        markdown_content += f"{idx}. {item}\n"

                    return markdown_content

            return '선택한 항목에 대한 참조 목록이 없습니다.'

        self.main_chatbot.select(update_citation, inputs=[
                                 chat_state], outputs=[citation_contents])

        self.user_check.change(
            toggle_resume_usage,
            inputs=[self.user_check, chat_state],
            outputs=[chat_state],
        )
