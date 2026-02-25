import uuid
from typing import Optional, Dict, Any, List
from app.domain.entities.audit import AuditLog, AuditAction
from app.domain.repositories.audit_repository import IAuditRepository

class LogAuditActionUseCase:
    """Caso de Uso: Grava um evento na trilha de auditoria (Caixa Preta)."""
    def __init__(self, audit_repository: IAuditRepository):
        self.audit_repository = audit_repository

    def execute(self, table_name: str, record_id: str, action: AuditAction,
                actor_id: Optional[uuid.UUID] = None, ip_address: Optional[str] = None,
                user_agent: Optional[str] = None, old_values: Optional[Dict[str, Any]] = None,
                new_values: Optional[Dict[str, Any]] = None) -> AuditLog:
        
        # Cria a entidade de Domínio (que fará as validações de coerência, como exigir old/new no UPDATE)
        log = AuditLog(
            table_name=table_name,
            record_id=record_id,
            action=action,
            actor_id=actor_id,
            ip_address=ip_address,
            user_agent=user_agent,
            old_values=old_values,
            new_values=new_values
        )
        
        # Salva o log de forma imutável (Append-Only)
        return self.audit_repository.save(log)

class GetRecordAuditHistoryUseCase:
    """Caso de Uso: Permite ao Admin ou ao Sistema recuperar a linha do tempo de um registo."""
    def __init__(self, audit_repository: IAuditRepository):
        self.audit_repository = audit_repository

    def execute(self, table_name: str, record_id: str) -> List[AuditLog]:
        if not table_name or not record_id:
            raise ValueError("O nome da tabela e o ID do registo são obrigatórios para a busca.")
            
        return self.audit_repository.get_by_record(table_name=table_name, record_id=record_id)