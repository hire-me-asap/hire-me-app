# 파일명: generate_id_card.py

import os
import requests
from PIL import Image, ImageDraw, ImageFont

def generate_avatar_id_card(seed: str, job: str, font_path: str = "NeoDunggeunmoPro-Regular.ttf") -> str:
    avatar_dir = "./avatars"
    card_dir = "./ID_Card"
    os.makedirs(avatar_dir, exist_ok=True)
    os.makedirs(card_dir, exist_ok=True)

    # 아바타 가져오기
    url = f"https://api.dicebear.com/9.x/pixel-art/png?seed={seed}&size=100"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Avatar fetch failed")

    avatar_path = os.path.join(avatar_dir, f"{seed}.png")
    with open(avatar_path, "wb") as f:
        f.write(response.content)

    # ID 카드 생성
    card_width, card_height = 360, 160
    avatar_size = 100
    padding = 12

    card = Image.new("RGB", (card_width, card_height), "#ffffff")
    draw = ImageDraw.Draw(card)
    draw.rectangle([(0, 0), (card_width - 1, card_height - 1)], outline="black", width=4)

    avatar = Image.open(avatar_path).resize((avatar_size, avatar_size))
    card.paste(avatar, (padding, padding))

    font = ImageFont.truetype(font_path, size=16)
    font_bold = ImageFont.truetype(font_path, size=18)

    text_x = avatar_size + 3 * padding
    text_y = padding
    draw.text((text_x, text_y), "▶ USER ID", font=font, fill="black")
    draw.text((text_x, text_y + 22), f"{seed}", font=font_bold, fill="black")

    draw.text((text_x, text_y + 54), "▶ WANTED POSITION", font=font, fill="black")
    draw.text((text_x, text_y + 76), f"{job}", font=font_bold, fill="black")

    draw.rectangle([(10, card_height - 20), (card_width - 10, card_height - 10)], fill="black")
    draw.text((card_width // 2 - 40, card_height - 20), "▶▶◼◼◼◼◼◼◼◼▶▶", font=font, fill="white")

    card_path = os.path.join(card_dir, "retro_id_card.png")
    card.save(card_path)

    return card_path