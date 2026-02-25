import pytest
import uuid
from app.domain.entities.audit import AuditLog, AuditAction
from app.infrastructure.repositories.audit_repository_impl import AuditRepositoryImpl

def test_deve_retornar_historico_de_auditoria_via_api(client, db_session):
    # 1. SETUP: Inserir um log diretamente via repositório (Simulando o sistema interno)
    repo = AuditRepositoryImpl(db_session)
    alvo_id = str(uuid.uuid4())
    admin_id = uuid.uuid4()
    
    log1 = AuditLog(
        table_name="orders",
        record_id=alvo_id,
        action=AuditAction.CREATE,
        actor_id=admin_id,
        new_values={"status": "CREATED", "total_amount": 100.0}
    )
    repo.save(log1)
    
    log2 = AuditLog(
        table_name="orders",
        record_id=alvo_id,
        action=AuditAction.UPDATE,
        actor_id=admin_id,
        old_values={"status": "CREATED"},
        new_values={"status": "PAID"}
    )
    repo.save(log2)

    # 2. ACTION: O Admin chama a API para ver o que aconteceu com este pedido
    resp = client.get(f"/audit/orders/{alvo_id}")

    # 3. ASSERT: Validar o retorno
    assert resp.status_code == 200
    data = resp.json()
    
    assert len(data) == 2
    # O mais recente primeiro (UPDATE)
    assert data[0]["action"] == "UPDATE"
    assert data[0]["new_values"]["status"] == "PAID"
    assert data[0]["old_values"]["status"] == "CREATED"
    
    # O mais antigo depois (CREATE)
    assert data[1]["action"] == "CREATE"
    assert data[1]["new_values"]["total_amount"] == 100.0