import os
import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.types import TypeDecorator, CHAR
from sqlalchemy.dialects.postgresql import UUID

# Pega a URL do banco do .env, se não existir, usa um SQLite local
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

# O SQLite precisa dessa flag extra para trabalhar bem com múltiplas threads no FastAPI
connect_args = {"check_same_thread": False} if "sqlite" in SQLALCHEMY_DATABASE_URL else {}

# Cria o motor que gerencia a conexão com o banco
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

# Cria a fábrica de sessões do banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# A classe Base que todos os nossos Models vão herdar
Base = declarative_base()

def get_db():
    """
    Função utilitária (Dependency) para o FastAPI.
    Garante que a sessão do banco seja aberta a cada requisição e fechada no final.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class GUID(TypeDecorator):
    """
    Tipo customizado para ID universal.
    Usa o tipo nativo UUID no PostgreSQL e um CHAR de 32 caracteres no SQLite.
    Isso garante que o mesmo código funcione em Dev e Prod sem alterações!
    """
    impl = CHAR
    cache_ok = True

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(UUID(as_uuid=True))
        else:
            return dialect.type_descriptor(CHAR(32))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid.UUID):
                return "%.32x" % uuid.UUID(value).int
            else:
                return "%.32x" % value.int

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            if not isinstance(value, uuid.UUID):
                value = uuid.UUID(value)
            return value