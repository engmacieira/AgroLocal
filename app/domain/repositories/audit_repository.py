from abc import ABC, abstractmethod
from typing import List
from app.domain.entities.audit import AuditLog

class IAuditRepository(ABC):
    @abstractmethod
    def save(self, audit_log: AuditLog) -> AuditLog:
        pass

    @abstractmethod
    def get_by_record(self, table_name: str, record_id: str) -> List[AuditLog]:
        """Traz todo o histórico de alterações de um registro específico (ex: ID de uma Ordem)."""
        pass