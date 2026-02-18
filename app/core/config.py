import os
from typing import List, Union
from pydantic import AnyHttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Metadados
    PROJECT_NAME: str = "AgroLocal"
    API_V1_STR: str = "/api/v1"
    
    # --- Banco de Dados (PostgreSQL) ---
    # Se não houver var de ambiente, tentamos conectar no padrão do Docker local
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://agrolocal_user:agrolocal_pass@localhost:5434/agrolocal"
    )

    # --- Segurança (JWT) ---
    SECRET_KEY: str = os.getenv("SECRET_KEY", "troque_isso_por_algo_seguro_em_producao")
    ALGORITHM: str = "HS256"
    # 60 minutos * 24 horas * 7 dias = 1 semana
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7

    # --- CORS (Cross-Origin Resource Sharing) ---
    # Lista de domínios permitidos para conversar com o backend
    # Aceita string separada por vírgula ou lista JSON
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    # --- Futuro: Integrações (Prepare o terreno) ---
    # PAGARME_API_KEY: str = ""
    # AWS_BUCKET_NAME: str = ""

    # Configuração do Pydantic para ler o .env automaticamente
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore" # Ignora variáveis extras no .env que não estão mapeadas aqui
    )

settings = Settings()