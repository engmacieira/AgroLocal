import pytest
import uuid
from app.domain.entities.audit import AuditLog, AuditAction

def test_deve_criar_log_de_auditoria_valido_para_criacao():
    user_id = uuid.uuid4()
    record_uuid = str(uuid.uuid4())
    
    log = AuditLog(
        table_name="orders",
        record_id=record_uuid,
        action=AuditAction.CREATE,
        actor_id=user_id,
        ip_address="192.168.1.100",
        new_values={"status": "CREATED", "total_amount": 150.0}
    )
    
    assert log.action == AuditAction.CREATE
    assert log.table_name == "orders"
    assert log.old_values is None # Num CREATE, não há valores antigos
    assert log.new_values["status"] == "CREATED"

def test_deve_exigir_old_e_new_values_em_caso_de_update():
    user_id = uuid.uuid4()
    
    # Tenta fazer um UPDATE sem informar o que mudou
    with pytest.raises(ValueError, match="Para a ação UPDATE, os campos old_values e new_values são obrigatórios"):
        AuditLog(
            table_name="producer_products",
            record_id=str(uuid.uuid4()),
            action=AuditAction.UPDATE,
            actor_id=user_id,
            old_values={"price": 10.0}
            # Faltou o new_values!
        )

def test_deve_higienizar_ip_e_user_agent():
    log = AuditLog(
        table_name="users",
        record_id=str(uuid.uuid4()),
        action=AuditAction.LOGIN,
        ip_address="   10.0.0.1   ",
        user_agent="   Mozilla/5.0   "
    )
    
    # O domínio deve limpar espaços extra
    assert log.ip_address == "10.0.0.1"
    assert log.user_agent == "Mozilla/5.0"