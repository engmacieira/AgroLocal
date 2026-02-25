import uuid
from typing import Optional
from app.domain.entities.communication import Conversation, SubjectType, ParticipantRole
from app.domain.repositories.communication_repository import ICommunicationRepository

class StartConversationUseCase:
    """Caso de Uso: Inicia um novo chamado/conversa já com a primeira mensagem."""
    def __init__(self, communication_repository: ICommunicationRepository):
        self.communication_repository = communication_repository

    def execute(self, initiator_id: uuid.UUID, target_id: uuid.UUID, subject_type: SubjectType, 
                initiator_role: ParticipantRole, target_role: ParticipantRole, 
                initial_message: str, reference_id: Optional[uuid.UUID] = None) -> Conversation:
        
        # 1. Cria o Tópico (Cabeçalho)
        conversa = Conversation(
            initiator_id=initiator_id,
            target_id=target_id,
            subject_type=subject_type,
            reference_id=reference_id,
            target_role=target_role
        )
        
        # 2. Adiciona a mensagem inicial (Corpo)
        conversa.add_message(
            sender_id=initiator_id,
            sender_role=initiator_role,
            content=initial_message
        )
        
        # 3. Salva tudo em cascata
        return self.communication_repository.save(conversa)

class SendMessageUseCase:
    """Caso de Uso: Adiciona uma nova mensagem a um chamado existente."""
    def __init__(self, communication_repository: ICommunicationRepository):
        self.communication_repository = communication_repository

    def execute(self, conversation_id: uuid.UUID, sender_id: uuid.UUID, 
                sender_role: ParticipantRole, content: str) -> Conversation:
        
        conversa = self.communication_repository.get_by_id(conversation_id)
        if not conversa:
            raise ValueError("Conversa/Chamado não encontrado")

        conversa.add_message(
            sender_id=sender_id,
            sender_role=sender_role,
            content=content
        )
        
        return self.communication_repository.save(conversa)

class CloseConversationUseCase:
    """Caso de Uso: Encerra o ticket."""
    def __init__(self, communication_repository: ICommunicationRepository):
        self.communication_repository = communication_repository

    def execute(self, conversation_id: uuid.UUID) -> Conversation:
        conversa = self.communication_repository.get_by_id(conversation_id)
        if not conversa:
            raise ValueError("Conversa/Chamado não encontrado")

        conversa.close_conversation()
        return self.communication_repository.save(conversa)