import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "AgroLocal"
    API_V1_STR: str = "/api/v1"
    
    # Database
    # Por padrão usa SQLite se não houver variável definida
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./app.db")

    # Security (Isso será usado na Sprint de Auth, mas já deixamos pronto)
    SECRET_KEY: str = os.getenv("SECRET_KEY", "troque_isso_por_algo_seguro")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 1 semana

    class Config:
        case_sensitive = True

settings = Settings()