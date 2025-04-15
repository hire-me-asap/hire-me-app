from fastapi import FastAPI
import uvicorn
import gradio as gr
from pathlib import Path
from src.ui.app import demo, sign_in_or_sign_up, AUTH_MESSAGE

app = FastAPI()
app = gr.mount_gradio_app(app, demo, path='',
    auth=sign_in_or_sign_up,
    auth_message=AUTH_MESSAGE,
    allowed_paths=[
        Path.cwd().absolute()/"resources",
        Path.cwd().absolute()/"static",
    ]
)

if __name__ == "__main__":
    # 외부 오픈을 하려면 host 를 "0.0.0.0" 으로 bind 해야 함.
    # uvicorn.run(app, host="127.0.0.1", port=8000)  # FastAPI 서버를 실행

    demo.launch(
        auth=sign_in_or_sign_up,
        auth_message=AUTH_MESSAGE,
        allowed_paths=[
            Path.cwd().absolute()/"resources",
            Path.cwd().absolute()/"static",
        ]
    )
