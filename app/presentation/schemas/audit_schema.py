from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict, Any
from uuid import UUID
from datetime import datetime
from app.domain.entities.audit import AuditAction

class AuditLogResponse(BaseModel):
    id: UUID
    table_name: str
    record_id: str
    action: AuditAction
    actor_id: Optional[UUID]
    ip_address: Optional[str]
    user_agent: Optional[str]
    old_values: Optional[Dict[str, Any]]
    new_values: Optional[Dict[str, Any]]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)