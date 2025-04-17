from fastapi import Request
import uuid
import gradio as gr
import re

from src.logic.app_logic import app_logic

AUTH_MESSAGE = (
    '<p><b>새 계정</b>으로 가입하거나 <b>기존 계정</b>으로 로그인하세요.</p><p><nbsp></p>'
    '<p>&#8203;</p>'
    '<p>아이디와 비밀번호는 <b>길이가 4 이상</b>이어야 하고<br/>'
    '<b>영문자, 숫자, 언더바</b>로만 구성되어야 합니다.</p>'
    '<p>&#8203;</p>'
    '<p><b>[로그인]</b> 버튼을 클릭하고 잠시 기다려주세요</p>'
    '<p>첫 가입 시에는 리소스 할당에 1분 정도 소요될 수 있습니다.</p>'
)

account_pattern = re.compile(r'^[A-Za-z\d_]{4,}$')


def sign_in_or_sign_up(user_id: str, password: str) -> bool:
    if not account_pattern.fullmatch(user_id) or not account_pattern.fullmatch(password):
        return False

    logged_in, message = app_logic.sign_in(user_id, password)
    if logged_in:
        return True

    if message == '아이디가 존재하지 않습니다.':
        app_logic.sign_up(user_id, password)
        return True

    return False

# 세션 저장소
sessions: dict[str, dict] = {}

# 세션 관리 함수
def get_session_id(request: Request):
    session_id = request.cookies.get("session_id")
    if not session_id or session_id not in sessions:
        session_id = str(uuid.uuid4())
        sessions[session_id] = {"created": True}
    return session_id

# Gradio 함수들
def on_login_success(username, request: gr.Request):
    # 쿠키에서 세션 ID 가져오기
    session_id = request.cookies.get("session_id")
    if session_id and session_id in sessions:
        sessions[session_id]["username"] = username
        sessions[session_id]["logged_in"] = True
        # return f"{username}님 로그인 성공!"
        print(f"{username}님 로그인 성공!")
        return
    # return "세션이 만료되었습니다."
    print("세션이 만료되었습니다.")
