import gradio as gr

def set_topbar_visibility(is_visible):
    return gr.update(visible=is_visible)