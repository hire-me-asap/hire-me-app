from pathlib import Path

from src.ui.app import demo, sign_in_or_sign_up, AUTH_MESSAGE

# Gradio 앱을 마운트하기 전에 인증 및 경로 설정을 적용
demo.auth = sign_in_or_sign_up
demo.auth_message = AUTH_MESSAGE
demo.allowed_paths = [
    Path.cwd().absolute()/"resources",
    Path.cwd().absolute()/"static",
]

if __name__ == "__main__":
    demo.launch()
