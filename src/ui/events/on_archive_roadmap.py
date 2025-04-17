import gradio as gr

from src.logic.app_logic import app_logic


def load_archive_images():
    """
    아카이브 섹션에 로드맵 이미지 리스트를 로드합니다.
    """
    try:
        # 이미지 리스트 가져오기
        image_list = app_logic.get_roadmap_image_list()
        # print(image_list)  # 디버깅용 출력
        return image_list, gr.update(open=bool(image_list))
    except ValueError as e:
        return [f"Error: {str(e)}"], gr.update()
