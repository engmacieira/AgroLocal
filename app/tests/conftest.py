import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from typing import Generator

from app.core.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient

# --- IMPORTANTE: Importar TODOS os models para o SQLAlchemy conhecê-los ---
# Sem isso, os relacionamentos (relationship="Address") falham pois a classe não foi lida.
from app.models import (
    user_model,
    address_model,
    catalog_model,
    product_model,
    order_model,
    transaction_model,
    payout_model,
    review_model,
    audit_model
)

# Banco SQLite em memória (Rápido e isolado)
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# Configuração específica para SQLite em memória funcionar com múltiplas threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session() -> Generator:
    """
    Fixture que cria um banco novo e limpo para CADA teste.
    """
    # 1. Cria todas as tabelas (Agora ele conhece todos os models importados acima!)
    Base.metadata.create_all(bind=engine)
    
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # 2. Destrói tudo ao final do teste
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """
    Cliente HTTP simulado que usa o banco de teste.
    """
    # Sobrescreve a dependência get_db para usar nosso banco em memória
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
            
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as c:
        yield c