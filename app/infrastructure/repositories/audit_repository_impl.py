from typing import List
from sqlalchemy.orm import Session
from app.domain.entities.audit import AuditLog
from app.domain.repositories.audit_repository import IAuditRepository
from app.infrastructure.models.audit_model import AuditModel

class AuditRepositoryImpl(IAuditRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def _to_domain(self, model: AuditModel) -> AuditLog:
        return AuditLog(
            id=model.id,
            table_name=model.table_name,
            record_id=model.record_id,
            action=model.action,
            actor_id=model.actor_id,
            ip_address=model.ip_address,
            user_agent=model.user_agent,
            old_values=model.old_values,
            new_values=model.new_values,
            created_at=model.created_at
        )

    def save(self, audit_log: AuditLog) -> AuditLog:
        model = AuditModel(
            id=audit_log.id,
            table_name=audit_log.table_name,
            record_id=audit_log.record_id,
            action=audit_log.action,
            actor_id=audit_log.actor_id,
            ip_address=audit_log.ip_address,
            user_agent=audit_log.user_agent,
            old_values=audit_log.old_values,
            new_values=audit_log.new_values,
            created_at=audit_log.created_at
        )
        self.db.add(model) # Adicionamos diretamente (Append-Only)
        self.db.commit()
        return audit_log

    def get_by_record(self, table_name: str, record_id: str) -> List[AuditLog]:
        models = self.db.query(AuditModel).filter(
            AuditModel.table_name == table_name,
            AuditModel.record_id == record_id
        ).order_by(AuditModel.created_at.desc()).all() # Mais recentes primeiro
        
        return [self._to_domain(m) for m in models]