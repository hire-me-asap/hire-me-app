import gradio as gr


def select_example(selected: gr.SelectData):
    return selected.value['text']
