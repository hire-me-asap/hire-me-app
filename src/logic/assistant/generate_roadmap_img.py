import json
import io
import os

from typing import Tuple, Union
from graphviz import Digraph
from PIL import Image

FONT = 'NeoDunggeunmo Pro'
STATIC_ROADMAP_DIR = "static/roadmap"  # 저장 경로 설정


def split_text_and_json(text: str, user_id: str, message_id: str) -> Tuple[str, str]:
    """
    입력된 문자열에서 일반 텍스트와 JSON 데이터를 분리하고,
    JSON 데이터를 기반으로 career roadmap 이미지를 생성합니다.

    Args:
        text (str): 전체 응답 텍스트. ---json start---로 일반 텍스트와 JSON이 구분되어 있어야 합니다.
        user_id (str): 저장을 위한 유저 아이디
        message_id (str): 중복 저장을 막기 위한 메세지 id

    Returns:
        Tuple[str, str]: 일반 텍스트와 생성된 이미지 경로 (또는 에러 메시지 문자열)
    """
    split_marker = "---json start---"
    if split_marker not in text:
        return text.strip(), "❗ '---json start---' 구분자가 포함되어 있지 않아요."

    text_part, json_part = text.split(split_marker, 1)
    text_part = text_part.strip()

    json_start = json_part.find('{')
    json_end = json_part.rfind('}') + 1
    json_string = json_part[json_start:json_end]

    try:
        image_path = _render_career_roadmap(json_string, user_id, message_id)
        return text_part, image_path
    except Exception as e:
        return text_part, f"⚠️ 이미지 생성 실패: {str(e)}"


def _render_career_roadmap(json_input: str, user_id: str, message_id: str) -> str:
    """
    주어진 JSON 문자열을 기반으로 커리어 로드맵 그래프를 생성하고,
    static/roadmap 폴더에 세로(TB) 방향 이미지를 저장합니다.

    Args:
        json_input (str): 노드와 연결 정보를 포함한 JSON 문자열
        user_id (str): 저장을 위한 유저 아이디
        message_id (str): 중복 저장을 막기 위한 메세지 id

    Returns:
        str: 성공 시 저장된 이미지 경로, 실패 시 오류 메시지
    """
    try:
        # JSON 파싱
        data = json.loads(json_input.strip())
        nodes = data["nodes"]

        # Graphviz 객체 생성
        dot = Digraph(comment=data.get(
            "title", "Career Roadmap"), encoding='utf-8')
        dot.attr(rankdir='TB')  # 방향 설정 (세로)
        dot.attr('node', fontname=FONT)
        dot.attr('edge', fontname=FONT)

        # 노드 추가
        for node in nodes:
            label = f"{node['name']}\n" + "\n".join(node["details"])
            dot.node(node["name"], label)

        # 엣지 추가
        for node in nodes:
            for conn in node.get("connections", []):
                dot.edge(node["name"], conn)

        # 그래프를 PNG로 변환
        png_bytes = dot.pipe(format='png')
        image = Image.open(io.BytesIO(png_bytes))

        # static/roadmap 폴더에 저장
        if not os.path.exists(STATIC_ROADMAP_DIR):
            os.makedirs(STATIC_ROADMAP_DIR)  # 폴더가 없으면 생성

        file_name = f"{user_id}_roadmap_{message_id}.png"
        file_path = os.path.join(STATIC_ROADMAP_DIR, file_name)

        # 경로를 슬래시(/)로 변환
        file_path = file_path.replace("\\", "/")

        image.save(file_path)
        return file_path

    except Exception as e:
        return f"⚠️ JSON 파싱 오류: {str(e)}"
