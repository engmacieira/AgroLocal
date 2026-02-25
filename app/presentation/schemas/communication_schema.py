from pydantic import BaseModel, ConfigDict, Field
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from app.domain.entities.communication import SubjectType, ParticipantRole, ConversationStatus

# --- REQUESTS ---

class StartConversationRequest(BaseModel):
    initiator_id: UUID
    target_id: UUID
    subject_type: SubjectType
    reference_id: Optional[UUID] = Field(None, description="ID do Pedido ou Produto, se aplicável")
    initiator_role: ParticipantRole
    target_role: ParticipantRole
    initial_message: str = Field(..., min_length=1, description="A primeira mensagem do chamado")

class SendMessageRequest(BaseModel):
    sender_id: UUID
    sender_role: ParticipantRole
    content: str = Field(..., min_length=1)

# --- RESPONSES ---

class MessageResponse(BaseModel):
    id: UUID
    sender_id: UUID
    sender_role: ParticipantRole
    content: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)

class ConversationResponse(BaseModel):
    id: UUID
    initiator_id: UUID
    target_id: UUID
    subject_type: SubjectType
    reference_id: Optional[UUID]
    target_role: ParticipantRole
    status: ConversationStatus
    messages: List[MessageResponse] = []
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)