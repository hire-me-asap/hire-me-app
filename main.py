from pathlib import Path

from src.ui.app import demo, sign_in_or_sign_up, AUTH_MESSAGE

if __name__ == "__main__":
    demo.launch(
        auth=sign_in_or_sign_up,
        auth_message=AUTH_MESSAGE,
        allowed_paths=[
            Path.cwd().absolute()/"resources",
            Path.cwd().absolute()/"static",
        ]
    )
