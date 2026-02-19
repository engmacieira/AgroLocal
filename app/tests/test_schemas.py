import pytest
from pydantic import ValidationError
from decimal import Decimal
from uuid import uuid4

from app.schemas.user_schema import UserCreate, UserRead
from app.schemas.product_schema import ProducerProductCreate
from app.models.user_model import UserRole

# --- Testes de Usuário (UserSchema) ---

def test_user_create_valid_data():
    """Testa se um payload válido passa na validação."""
    payload = {
        "email": "teste@valido.com",
        "full_name": "Usuario Teste",
        "password": "senha_forte_123",
        "role": "CLIENTE"
    }
    user = UserCreate(**payload)
    assert user.email == "teste@valido.com"
    assert user.password == "senha_forte_123"

def test_user_create_invalid_email():
    """Testa se o Pydantic barra e-mail sem @."""
    payload = {
        "email": "email_sem_arroba",
        "full_name": "Usuario Errado",
        "password": "senha123",
        "role": "CLIENTE"
    }
    # Esperamos que levante um ValidationError
    with pytest.raises(ValidationError) as excinfo:
        UserCreate(**payload)
    
    # Verifica se o erro menciona o campo 'email'
    errors = excinfo.value.errors()
    assert any(e["loc"] == ("email",) for e in errors)

def test_user_create_short_password():
    """Testa se barra senha com menos de 8 caracteres."""
    payload = {
        "email": "teste@curto.com",
        "full_name": "Senha Curta",
        "password": "123", # Muito curta
        "role": "CLIENTE"
    }
    with pytest.raises(ValidationError) as excinfo:
        UserCreate(**payload)
    
    # O erro deve ser no campo password
    errors = excinfo.value.errors()
    assert any(e["loc"] == ("password",) for e in errors)

def test_user_read_security():
    """Garante que o Schema de Leitura NÃO expõe a senha."""
    # Simulamos um objeto do banco de dados (pode ser um dict ou objeto)
    db_user = {
        "id": uuid4(),
        "email": "user@secure.com",
        "password_hash": "hash_secreto_que_nao_pode_vazar",
        "full_name": "Seguro",
        "role": UserRole.CLIENTE,
        "is_active": True,
        "is_verified": True
    }
    
    # Convertemos para o Schema de Resposta
    user_read = UserRead.model_validate(db_user)
    
    # Verifica se os dados públicos estão lá
    assert user_read.email == "user@secure.com"
    
    # Verifica se a senha ou hash NÃO existem no objeto de resposta
    assert not hasattr(user_read, "password")
    assert not hasattr(user_read, "password_hash")

# --- Testes de Produto (ProductSchema) ---

def test_product_price_validation():
    """Testa validação de preços e conversão Decimal."""
    # Preço válido
    prod = ProducerProductCreate(
        global_product_id=uuid4(),
        price=10.50, # Float deve converter para Decimal
        stock_quantity=10
    )
    assert isinstance(prod.price, Decimal)
    assert prod.price == Decimal("10.50")

    # Preço Negativo (O Pydantic por padrão aceita negativo no Decimal, 
    # a menos que usemos Field(ge=0). Vamos testar se o nosso schema permite ou não.
    # Se você não colocou ge=0 no Schema, este teste vai PASSAR sem erro, 
    # o que indica que PRECISAMOS melhorar o Schema!)
    
    # Nota: No seu schema atual, usamos apenas Decimal. 
    # Vamos criar um cenário que deveria falhar se adicionarmos validação futura.
    # Por enquanto, vamos apenas validar que ele aceita e converte tipos.

def test_product_required_fields():
    """Testa se campos obrigatórios faltando geram erro."""
    # Faltando o preço
    payload = {
        "global_product_id": uuid4(),
        "stock_quantity": 10
    }
    with pytest.raises(ValidationError):
        ProducerProductCreate(**payload)