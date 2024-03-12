# 全局配置信息
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    WEB_HOST: Optional[str] = Field('0.0.0.0', title="web主机")
    WEB_PORT: Optional[int] = Field(8000, title="web主机端口")


    OPENAI_API_KEY: Optional[str]
    CODE: Optional[str]
    PROXY_URL: Optional[str]

    BASE_URL: str = 'https://api.openai.com'
    OPENAI_ORG_ID: Optional[str]

    HIDE_USER_API_KEY: Optional[bool] = False
    DISABLE_GPT4: Optional[bool] = False

    class Config:
        env_file = ".env"

    @lru_cache(maxsize=None)
    def get(self, name: str):
        return getattr(self, name)


settings = Settings()
