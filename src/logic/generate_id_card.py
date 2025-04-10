# 파일명: generate_id_card.py

import os
import requests
from PIL import Image, ImageDraw, ImageFont


def generate_avatar_id_card(
    seed: str, job: Optional[str], font_path: str = "NeoDunggeunmoPro-Regular.ttf"
) -> str:
    avatar_dir = "./static/avatars"
    card_dir = "./static/ID_Card"
    os.makedirs(avatar_dir, exist_ok=True)
    os.makedirs(card_dir, exist_ok=True)

    # avatar
    url = f"https://api.dicebear.com/9.x/pixel-art/png?seed={seed}&size=100"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Avatar fetch failed")
    avatar_path = os.path.join(avatar_dir, f"{seed}.png")
    with open(avatar_path, "wb") as f:
        f.write(response.content)

    # card image
    card = Image.new("RGB", (360, 160), "#ffffff")
    draw = ImageDraw.Draw(card)
    draw.rectangle([(0, 0), (359, 159)], outline="black", width=4)

    avatar = Image.open(avatar_path).resize((100, 100))
    card.paste(avatar, (12, 12))

    font = ImageFont.truetype(font_path, size=16)
    font_bold = ImageFont.truetype(font_path, size=18)

    draw.text((text_x, text_y), "▶ USER ID", font=font, fill="black")
    draw.text((text_x, text_y + 22), f"{seed}", font=font_bold, fill="black")
    draw.text((text_x, text_y + 54), "▶ WANTED POSITION", font=font, fill="black")
    draw.text((text_x, text_y + 76), f"{job}", font=font_bold, fill="black")

    draw.rectangle(
        [(10, card_height - 20), (card_width - 10, card_height - 10)], fill="black"
    )
    draw.text(
        (card_width // 2 - 40, card_height - 20),
        "▶▶◼◼◼◼◼◼◼◼▶▶",
        font=font,
        fill="white",
    )

    card_path = os.path.join(card_dir, f"{seed}.png")
    card.save(card_path)

    # 반환용: 웹에서 접근 가능한 경로
    return f"/static/ID_Card/{seed}.png"
