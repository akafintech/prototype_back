from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # SQLite 데이터베이스 사용 (개발용)
    database_url: str = "sqlite:///./lemong.db"
    secret_key: str = "your-secret-key-here-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60*24
    
    # OpenAI API 설정
    openai_api_key: str = "sk-your-actual-openai-api-key-here"
    
    class Config:
        env_file = ".env"

settings = Settings() 