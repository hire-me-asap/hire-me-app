from fastapi import FastAPI
from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import gradio as gr
from pathlib import Path
from src.ui import demo, sign_in_or_sign_up, AUTH_MESSAGE
from src.ui import get_session_id, sessions

app = FastAPI()

# CORS 미들웨어 추가
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 또는 ["https://your-frontend-url"]로 제한
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 세션 쿠키 설정 미들웨어
@app.middleware("http")
async def session_middleware(request: Request, call_next):
    session_id = get_session_id(request)
    response = await call_next(request)
    response.set_cookie(key="session_id", value=session_id)
    return response

# FastAPI 엔드포인트로 세션 정보 확인
@app.get("/api/session-info", response_class=HTMLResponse)
async def session_info(session_id: str = Depends(get_session_id)):
    session_data = sessions.get(session_id, {})
    return f"""
    <html>
        <body>
            <h1>세션 정보</h1>
            <p>세션 ID: {session_id}</p>
            <p>데이터: {session_data}</p>
        </body>
    </html>
    """

app = gr.mount_gradio_app(
    app,
    demo,
    path='',
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
        ],
        favicon_path='resources/icon.png'
    )
