from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.infrastructure.repositories.communication_repository_impl import CommunicationRepositoryImpl

from app.application.use_cases.communication_management import (
    StartConversationUseCase, SendMessageUseCase, CloseConversationUseCase
)
from app.presentation.schemas.communication_schema import (
    StartConversationRequest, SendMessageRequest, ConversationResponse
)

router = APIRouter(prefix="/conversations", tags=["Communication (Chat & Chamados)"])

@router.post("/", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def start_conversation(request: StartConversationRequest, db: Session = Depends(get_db)):
    """Inicia um novo chamado/conversa com uma mensagem inicial."""
    repo = CommunicationRepositoryImpl(db)
    use_case = StartConversationUseCase(repo)
    
    try:
        return use_case.execute(
            initiator_id=request.initiator_id, target_id=request.target_id,
            subject_type=request.subject_type, initiator_role=request.initiator_role,
            target_role=request.target_role, initial_message=request.initial_message,
            reference_id=request.reference_id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{conversation_id}/messages", response_model=ConversationResponse)
def send_message(conversation_id: UUID, request: SendMessageRequest, db: Session = Depends(get_db)):
    """Adiciona uma resposta a uma conversa existente."""
    repo = CommunicationRepositoryImpl(db)
    use_case = SendMessageUseCase(repo)
    
    try:
        return use_case.execute(
            conversation_id=conversation_id, sender_id=request.sender_id,
            sender_role=request.sender_role, content=request.content
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{conversation_id}/close", response_model=ConversationResponse)
def close_conversation(conversation_id: UUID, db: Session = Depends(get_db)):
    """Encerra um ticket (Ninguém mais pode enviar mensagens)."""
    repo = CommunicationRepositoryImpl(db)
    use_case = CloseConversationUseCase(repo)
    
    try:
        return use_case.execute(conversation_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/user/{user_id}", response_model=List[ConversationResponse])
def get_user_conversations(user_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista o histórico de chamados (Caixa de Entrada) de um utilizador."""
    repo = CommunicationRepositoryImpl(db)
    return repo.get_conversations_by_user(user_id, skip, limit)