import gradio as gr

from src.ui.constants import *
from src.ui.events import select_example, process_user_message


class ChatbotTab:
    def __init__(self):
        with gr.Tab('엣취', id=0, elem_id='chatbot-tab') as chatbot_tab:
            self.main_chatbot = gr.Chatbot(
                [],
                elem_id="chatbot",
                label=FEATURES[Modes.GENERAL],
                type='messages',
                examples=EXAMPLE_MESSAGES[Modes.GENERAL],
            )
            self.user_check = gr.CheckboxGroup(
                ['📜 이력서 포함시키기', '이런 식으로 체크박스', '여러 개 넣을 수 있어요'],
                show_label=False,
                elem_id="custom-checkbox"
            )
            self.input_textarea = gr.TextArea(
                placeholder='❔ 엣취에게 물어보세요',
                elem_id='user-input-txt',
                lines=1,
                max_lines=5,
                submit_btn=True,
                show_label=False
            )
            gr.Markdown('엣취는 실수를 할 수 있습니다.', elem_id='etch_kawai')
        
        self.chatbot_tab = chatbot_tab
    
    def init_event_handlers(self, chat_state):
        self.main_chatbot.example_select(select_example, outputs=[self.input_textarea])
        
        self.input_textarea.submit(
            process_user_message,
            inputs=[self.input_textarea, chat_state],
            outputs=[self.input_textarea, self.main_chatbot, chat_state],
            scroll_to_output=True,
            queue=True
        )
        
        # TODO: 기능 구현 후에 아래 이벤트 핸들러는 제거해주세요. 
        def test_select(select_data: gr.SelectData, chat_state):
            history = chat_state['histories'][chat_state['mode']]
            idx = select_data.index
            
            if idx >= len(history):
                return
            
            message = history[idx]
            if 'citations' in message:
                print(f'@@@ Citational message: {message["citations"]}')
            else:
                print('@@@ No citations found.')
        
        self.main_chatbot.select(test_select, inputs=[chat_state])