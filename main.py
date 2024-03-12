import os

import uvicorn
from fastapi import FastAPI, Request
from rich.console import Console
from rich.table import Table
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from api.chat.router import chat_router
from api.config.router import config_router
from utils.all_utils import get_now
from settings.config import settings

# load_dotenv()

app = FastAPI(default_response_class=JSONResponse, default_encoding="utf-8")

# 配置允许的跨域请求来源和方法
# origins = [
#     "http://localhost",
#     "http://localhost:3000",
#     "http://localhost:8000",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/openai")
app.include_router(config_router, prefix="/config")


@app.get("/")
async def index():
    return "请使用 Web 前端访问，不支持直接访问。前端地址：https://zhb.chatools.online"


@app.middleware("http")
async def log_requests(request: Request, call_next):
    if request.method.lower() == "options":
        response = await call_next(request)
        return response

    headers = dict(request.headers)
    client_host = request.client.host
    print(
        f"FUCK ZHB ??*_*  :Time: {get_now()} | Host: {client_host} -> Request headers: \
        {headers['authorization'] if 'authorization' in headers else 'None'}")
    response = await call_next(request)
    return response


@app.on_event("startup")
async def startup_event():
    console = Console()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("OpenAI API Key", style="dim", width=40)
    table.add_column("CODE", width=40)
    table.add_row(settings.OPENAI_API_KEY, settings.CODE)
    console.print("You Config Info ⬇️⬇️⬇️")
    console.print(table)
    console.print("欢迎来到 ChatGPT-Next-Web For Python FastApi 😊😊😊")
    console.print("Star: https://github.com/iszhouhuabo/chatgpt-next-web-fastapi")

    # console.print(settings)


# 关闭时
@app.on_event("shutdown")
async def on_shutdown():
    console = Console()
    console.print("See You Again...")


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.WEB_HOST, port=settings.WEB_PORT, reload=False)
