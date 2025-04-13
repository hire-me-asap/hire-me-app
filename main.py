# import os
from fastapi import FastAPI
# from fastapi import Request
# from fastapi.responses import HTMLResponse, RedirectResponse
# from fastapi.staticfiles import StaticFiles
# from fastapi.templating import Jinja2Templates
import uvicorn
import gradio as gr
from hireme import demo

app = FastAPI()
# path='/gradio' 를 사용하여 하위 URL 로 만들고 아래의 코드처럼 루트(/) URL 은 다른 웹페이지를 서비스하게 만들 수도 있음.
app = gr.mount_gradio_app(app, demo, path='')

# @app.get("/")
# def read_root():
#     return {"Hello": "World"}

# os.makedirs("static", exist_ok=True)
# app.mount("/static", StaticFiles(directory="static"), name="static")
# templates = Jinja2Templates(directory="templates")
# videos = []
# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse(
#         "home.html", {"request": request, "videos": videos})

def main():
    # 외부 오픈을 하려면 host 를 "0.0.0.0" 으로 bind 해야 함.
    uvicorn.run(app, host="127.0.0.1", port=8000)  # FastAPI 서버를 실행

if __name__ == "__main__":
    main()
