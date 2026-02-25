from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.infrastructure.repositories.audit_repository_impl import AuditRepositoryImpl
from app.application.use_cases.audit_management import GetRecordAuditHistoryUseCase
from app.presentation.schemas.audit_schema import AuditLogResponse

router = APIRouter(prefix="/audit", tags=["Audit (Auditoria e Caixa Preta)"])

@router.get("/{table_name}/{record_id}", response_model=List[AuditLogResponse])
def get_audit_history(table_name: str, record_id: str, db: Session = Depends(get_db)):
    """Consulta a linha do tempo e o histórico de alterações de um registro específico."""
    repo = AuditRepositoryImpl(db)
    use_case = GetRecordAuditHistoryUseCase(repo)
    
    try:
        return use_case.execute(table_name=table_name, record_id=record_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))