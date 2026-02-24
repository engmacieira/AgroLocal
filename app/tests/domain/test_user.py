import pytest
from uuid import UUID
from datetime import datetime
from app.domain.entities.user import User, UserRole

def test_criar_novo_usuario_com_sucesso():
    user = User(
        email="produtor@agrolocal.com", 
        password_hash="hash", 
        full_name="João", 
        role=UserRole.PRODUTOR
    )
    assert isinstance(user.id, UUID)
    assert user.is_active is True
    assert user.is_verified is False

def test_usuario_pode_aceitar_termos_de_uso():
    user = User(email="teste@agrolocal.com", password_hash="hash", full_name="João")
    user.accept_terms()
    assert isinstance(user.terms_accepted_at, datetime)

def test_usuario_pode_verificar_conta():
    user = User(email="teste@agrolocal.com", password_hash="hash", full_name="João")
    user.verify_account()
    assert user.is_verified is True

def test_usuario_pode_registrar_ultimo_login():
    user = User(email="teste@agrolocal.com", password_hash="hash", full_name="João")
    user.register_login()
    assert isinstance(user.last_login, datetime)

def test_usuario_pode_ser_desativado_soft_delete():
    user = User(email="teste@agrolocal.com", password_hash="hash", full_name="João")
    user.deactivate()
    assert user.is_active is False