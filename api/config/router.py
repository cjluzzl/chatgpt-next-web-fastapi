from fastapi import APIRouter
from starlette.responses import JSONResponse

from settings.config import settings

config_router = APIRouter()


# 给前端的一些配置
@config_router.post("")
async def subscription() -> JSONResponse:
    return JSONResponse({"needCode": True if settings.CODE else False,
                         "hideUserApiKey": settings.HIDE_USER_API_KEY,
                         "enableGPT4": not settings.DISABLE_GPT4})
