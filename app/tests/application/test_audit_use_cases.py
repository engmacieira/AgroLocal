import pytest
import uuid
from app.domain.entities.audit import AuditLog, AuditAction
from app.domain.repositories.audit_repository import IAuditRepository
from app.application.use_cases.audit_management import LogAuditActionUseCase, GetRecordAuditHistoryUseCase

# --- FAKE REPOSITÓRIO ---
class FakeAuditRepository(IAuditRepository):
    def __init__(self): self.logs = []
    
    def save(self, audit_log):
        self.logs.append(audit_log)
        return audit_log
        
    def get_by_record(self, table_name, record_id):
        # Retorna os logs filtrados e ordenados (simulando a base de dados)
        filtrados = [log for log in self.logs if log.table_name == table_name and log.record_id == record_id]
        return sorted(filtrados, key=lambda x: x.created_at, reverse=True)

# --- TESTES ---
def test_deve_gravar_evento_de_auditoria_com_sucesso():
    repo = FakeAuditRepository()
    use_case = LogAuditActionUseCase(repo)
    
    admin_id = uuid.uuid4()
    produto_id = str(uuid.uuid4())
    
    log = use_case.execute(
        table_name="producer_products",
        record_id=produto_id,
        action=AuditAction.APPROVE,
        actor_id=admin_id,
        ip_address="127.0.0.1",
        new_values={"status": "APPROVED"}
    )
    
    assert log.action == AuditAction.APPROVE
    assert log.ip_address == "127.0.0.1"
    assert len(repo.logs) == 1

def test_deve_falhar_ao_tentar_gravar_update_sem_valores():
    repo = FakeAuditRepository()
    use_case = LogAuditActionUseCase(repo)
    
    with pytest.raises(ValueError, match="old_values e new_values são obrigatórios"):
        use_case.execute(
            table_name="orders",
            record_id=str(uuid.uuid4()),
            action=AuditAction.UPDATE
            # Esquecemos propositadamente os valores!
        )

def test_deve_recuperar_historico_de_um_registo():
    repo = FakeAuditRepository()
    log_uc = LogAuditActionUseCase(repo)
    get_uc = GetRecordAuditHistoryUseCase(repo)
    
    pedido_id = str(uuid.uuid4())
    
    # Grava dois eventos para o mesmo pedido
    log_uc.execute(table_name="orders", record_id=pedido_id, action=AuditAction.CREATE, new_values={"total": 100})
    log_uc.execute(table_name="orders", record_id=pedido_id, action=AuditAction.UPDATE, old_values={"status": "CREATED"}, new_values={"status": "PAID"})
    
    # Grava um evento para OUTRO pedido
    log_uc.execute(table_name="orders", record_id=str(uuid.uuid4()), action=AuditAction.CREATE, new_values={"total": 50})
    
    historico = get_uc.execute(table_name="orders", record_id=pedido_id)
    
    # Deve trazer apenas os 2 eventos do nosso pedido alvo
    assert len(historico) == 2