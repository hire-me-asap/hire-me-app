import json
import io

from typing import Tuple, Union
from graphviz import Digraph
from PIL import Image

FONT = 'NeoDunggeunmo Pro'


def split_text_and_json(text: str) -> Tuple[str, Union[Image.Image, str]]:
    """
    입력된 문자열에서 일반 텍스트와 JSON 데이터를 분리하고,
    JSON 데이터를 기반으로 career roadmap 이미지를 생성합니다.

    Args:
        text (str): 전체 응답 텍스트. ---json start---로 일반 텍스트와 JSON이 구분되어 있어야 합니다.

    Returns:
        Tuple[str, Union[Image.Image, str]]: 일반 텍스트와 생성된 이미지 (또는 에러 메시지 문자열)
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
        image = _render_career_roadmap(json_string)
    except Exception as e:
        image = f"⚠️ 이미지 생성 실패: {str(e)}"

    return text_part, image


def _render_career_roadmap(json_input: str) -> Union[Image.Image, str]:
    """
    주어진 JSON 문자열을 기반으로 커리어 로드맵 그래프를 생성합니다.

    JSON은 다음과 같은 구조여야 합니다:
    {
        "title": "로드맵 제목",
        "nodes": [
            {
                "name": "노드 이름",
                "details": ["세부내용1", "세부내용2"],
                "connections": ["연결된 노드1", "연결된 노드2"]
            },
            ...
        ]
    }

    Args:
        json_input (str): 노드와 연결 정보를 포함한 JSON 문자열

    Returns:
        Union[Image.Image, str]: 생성된 그래프 이미지 (PIL.Image) 또는 오류 메시지 (str)
    """
    try:
        data = json.loads(json_input.strip())
        nodes = data["nodes"]

        dot = Digraph(comment=data.get(
            "title", "Career Roadmap"), encoding='utf-8')
        dot.attr(rankdir='TB')  # 위에서 아래 방향 (세로 흐름)
        dot.attr('node', fontname=FONT)
        dot.attr('edge', fontname=FONT)

        for node in nodes:
            label = f"{node['name']}\n" + "\n".join(node["details"])
            dot.node(node["name"], label)

        for node in nodes:
            for conn in node.get("connections", []):
                dot.edge(node["name"], conn)

        try:
            png_bytes = dot.pipe(format='png')
            image = Image.open(io.BytesIO(png_bytes))
            return image
        except Exception as e:
            return f"⚠️ Graphviz 오류: {str(e)}"

    except Exception as e:
        return f"⚠️ JSON 파싱 오류: {str(e)}"
