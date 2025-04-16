import gradio as gr

from src.ui.components import ChatbotTab, ProfileTab
from src.logic.app_logic import app_logic


class TabHost:
    def __init__(self):
        with gr.Tabs() as tab_host:
            self.chatbot_tab_wrapper = ChatbotTab()
            self.profile_tab_wrapper = ProfileTab()

        self.tab_host = tab_host
        self.app_logic = app_logic

    def init_event_handlers(self, chat_state, citation_contents):
        self.chatbot_tab_wrapper.init_event_handlers(chat_state, citation_contents)
        self.profile_tab_wrapper.init_event_handlers()