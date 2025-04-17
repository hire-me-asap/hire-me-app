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

    def init_event_handlers(
        self,
        chat_state,
        citation_contents,
        real_name,
        summary,
        skill_stack,
        final_degree, 
        major, 
        school_name, 
        gpa, 
        degree_date, 
        education_exp, 
        work_experiences, 
        cerificates, 
        awards, 
        languages, 
        main_chatbot, 
        sidebarprofile, 
        archive_gallery,
        citation_accordian
    ):
        self.chatbot_tab_wrapper.init_event_handlers(
            chat_state, citation_contents, archive_gallery, self.profile_tab_wrapper.resume_info_temp, citation_accordian)
        self.profile_tab_wrapper.init_event_handlers(
            chat_state, real_name, summary, skill_stack, final_degree, major, school_name, gpa,
            degree_date, education_exp, work_experiences, cerificates, awards, languages, main_chatbot, sidebarprofile)
