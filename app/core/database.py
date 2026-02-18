import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID
from app.core.config import settings

# --- 1. Configuração da Engine (PostgreSQL) ---

engine = create_engine(settings.DATABASE_URL)

# --- 2. Sessão do Banco de Dados ---
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# --- 3. Tipo Customizado: GUID (UUID Universal) ---
class GUID(TypeDecorator):
    """
    Tipo GUID agnóstico de plataforma.
    
    Lógica Híbrida:
    - No PostgreSQL: Usa o tipo nativo UUID() (Mais eficiente e indexável).
    - Em outros bancos: Usa CHAR(36) como fallback.
    
    Isso permite que o código Python use objetos uuid.UUID transparentemente,
    sem se preocupar em converter para string manualmente.
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID())
        else:
            return dialect.type_descriptor(CHAR(36))

    def process_bind_param(self, value, dialect):
        """Converte o valor do Python para o Banco."""
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return str(uuid.UUID(value))
            return str(value)

    def process_result_value(self, value, dialect):
        """Converte o valor do Banco para o Python."""
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value

# --- 4. Injeção de Dependência ---
def get_db():
    """
    Dependency Generator para o FastAPI.
    Garante que a conexão abre e fecha a cada requisição.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()