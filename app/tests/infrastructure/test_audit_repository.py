import pytest
import uuid
from app.domain.entities.user import User
from app.domain.entities.audit import AuditLog, AuditAction
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.audit_repository_impl import AuditRepositoryImpl

def test_deve_salvar_e_recuperar_historico_de_auditoria(db_session):
    repo = AuditRepositoryImpl(db_session)
    user_repo = UserRepositoryImpl(db_session)
    
    # Setup: Criar um Admin para ser o 'ator'
    admin = user_repo.save(User(email="admin_auditoria@teste.com", password_hash="12345678", full_name="Admin Supremo"))
    
    # ID de um registro fictício que estamos auditando
    alvo_id = str(uuid.uuid4())
    
    # Ação 1: CREATE (Criação inicial)
    log_criacao = AuditLog(
        table_name="producer_products",
        record_id=alvo_id,
        action=AuditAction.CREATE,
        actor_id=admin.id,
        new_values={"name": "Cenoura", "price": 5.0}
    )
    repo.save(log_criacao)
    
    # Ação 2: UPDATE (Alteração de preço pelo Admin)
    log_atualizacao = AuditLog(
        table_name="producer_products",
        record_id=alvo_id,
        action=AuditAction.UPDATE,
        actor_id=admin.id,
        old_values={"name": "Cenoura", "price": 5.0},
        new_values={"name": "Cenoura", "price": 6.5}
    )
    repo.save(log_atualizacao)
    
    # Assert: Recuperar a linha do tempo
    historico = repo.get_by_record(table_name="producer_products", record_id=alvo_id)
    
    assert len(historico) == 2
    
    # O mais recente (UPDATE) deve vir primeiro devido à ordenação desc()
    assert historico[0].action == AuditAction.UPDATE
    assert historico[0].old_values["price"] == 5.0
    assert historico[0].new_values["price"] == 6.5
    
    # O mais antigo (CREATE) vem a seguir
    assert historico[1].action == AuditAction.CREATE
    assert historico[1].new_values["name"] == "Cenoura"
    assert historico[1].old_values is None