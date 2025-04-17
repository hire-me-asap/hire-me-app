import re
import gradio as gr

from pathlib import Path

from src.ui.theme import custom_theme
from src.ui.events import load_histories, update_sidebar_profile_image, load_archive_images, json_to_user_component
from src.ui.constants import *
from src.ui.components import LeftSidebar, RightSidebar, Topbar, TabHost, ProfileTab
from src.logic.app_logic import app_logic

gr.set_static_paths(paths=[
    Path.cwd().absolute()/"resources",
    Path.cwd().absolute()/"static",
])

with gr.Blocks(css_paths=['src/ui/style.css'], theme=custom_theme, title='엣취 - 엣지있게 취업하기') as demo:

    """ 
    컴포넌트 배치
    """
    left_sidebar_wrapper = LeftSidebar()
    right_sidebar_wrapper = RightSidebar()

    topbar_wrapper = Topbar()
    tab_host_wrapper = TabHost()

    """
    상태 변수
    """

    chat_state = gr.State({
        'mode': Modes.GENERAL,
        'histories': {
            Modes.GENERAL: [],
            Modes.JOB: [],
            Modes.RECRUIT: [],
            Modes.RESUME: [],
            Modes.ROADMAP: [],
            Modes.COURSE: [],
        },
        'use_resume': True
    })

    user_input_components = gr.State({})

    """
    이벤트 핸들러
    """

    # 앱 처음 실행시
    demo.load(
        update_sidebar_profile_image,
        inputs=[left_sidebar_wrapper.profile_image],
        outputs=[left_sidebar_wrapper.profile_image]
    ).then(
        load_histories,
        inputs=[chat_state],
        outputs=[
            chat_state,
            tab_host_wrapper.chatbot_tab_wrapper.main_chatbot,
            tab_host_wrapper.chatbot_tab_wrapper.input_textarea
        ]
    ).then(
        load_archive_images,
        inputs=[],
        outputs=[right_sidebar_wrapper.archive_gallery, right_sidebar_wrapper.archive_accordian]
    ).then(
        app_logic.get_resume_info, outputs=[user_input_components]
    ).then(
        json_to_user_component, inputs=[user_input_components], 
        outputs=[tab_host_wrapper.profile_tab_wrapper.real_name,
        tab_host_wrapper.profile_tab_wrapper.summary,
        tab_host_wrapper.profile_tab_wrapper.skill_stack,
        tab_host_wrapper.profile_tab_wrapper.final_degree,
        tab_host_wrapper.profile_tab_wrapper.major,
        tab_host_wrapper.profile_tab_wrapper.school_name,
        tab_host_wrapper.profile_tab_wrapper.gpa,
        tab_host_wrapper.profile_tab_wrapper.degree_date,
        tab_host_wrapper.profile_tab_wrapper.education_and_exp,
        tab_host_wrapper.profile_tab_wrapper.work_experiences,
        tab_host_wrapper.profile_tab_wrapper.certificates,
        tab_host_wrapper.profile_tab_wrapper.awards,
        tab_host_wrapper.profile_tab_wrapper.languages])


    # 각 컴포넌트의 이벤트 핸들러 초기화
    left_sidebar_wrapper.init_event_handlers(
        topbar_wrapper.topbar,
        tab_host_wrapper.tab_host,
        tab_host_wrapper.chatbot_tab_wrapper.main_chatbot,
        chat_state,
        tab_host_wrapper.profile_tab_wrapper.userid_text,
        tab_host_wrapper.profile_tab_wrapper.wanted_job,
        tab_host_wrapper.profile_tab_wrapper.profile_image        
    )
    topbar_wrapper.init_event_handler(
        chat_state,
        tab_host_wrapper.tab_host,
        tab_host_wrapper.chatbot_tab_wrapper.main_chatbot
    )
    tab_host_wrapper.init_event_handlers(
        chat_state,
        right_sidebar_wrapper.sidebar.citation.contents,
        tab_host_wrapper.profile_tab_wrapper.real_name,
        tab_host_wrapper.profile_tab_wrapper.summary,
        tab_host_wrapper.profile_tab_wrapper.skill_stack,
        tab_host_wrapper.profile_tab_wrapper.final_degree,
        tab_host_wrapper.profile_tab_wrapper.major,
        tab_host_wrapper.profile_tab_wrapper.school_name,
        tab_host_wrapper.profile_tab_wrapper.gpa,
        tab_host_wrapper.profile_tab_wrapper.degree_date,
        tab_host_wrapper.profile_tab_wrapper.education_and_exp,
        tab_host_wrapper.profile_tab_wrapper.work_experiences,
        tab_host_wrapper.profile_tab_wrapper.certificates,
        tab_host_wrapper.profile_tab_wrapper.awards,
        tab_host_wrapper.profile_tab_wrapper.languages,
        tab_host_wrapper.chatbot_tab_wrapper.main_chatbot,
        left_sidebar_wrapper.profile_image,
        right_sidebar_wrapper.archive_gallery,
        right_sidebar_wrapper.sidebar.citation,
        right_sidebar_wrapper.archive_accordian,
    )
    right_sidebar_wrapper.init_event_handlers()
