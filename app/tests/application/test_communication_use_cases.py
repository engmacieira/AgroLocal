import pytest
import uuid
from app.domain.entities.communication import Conversation, SubjectType, ParticipantRole, ConversationStatus
from app.domain.repositories.communication_repository import ICommunicationRepository
from app.application.use_cases.communication_management import (
    StartConversationUseCase, SendMessageUseCase, CloseConversationUseCase
)

# --- FAKE REPOSITÓRIO ---
class FakeCommunicationRepository(ICommunicationRepository):
    def __init__(self): self.conversations = []
    
    def save(self, conversation):
        self.conversations = [c for c in self.conversations if c.id != conversation.id]
        self.conversations.append(conversation)
        return conversation
        
    def get_by_id(self, conversation_id): 
        return next((c for c in self.conversations if c.id == conversation_id), None)
        
    def get_conversations_by_user(self, user_id, skip=0, limit=100): pass

# --- TESTES ---
def test_deve_iniciar_conversa_com_mensagem_inicial():
    repo = FakeCommunicationRepository()
    use_case = StartConversationUseCase(repo)
    
    conversa = use_case.execute(
        initiator_id=uuid.uuid4(), target_id=uuid.uuid4(),
        subject_type=SubjectType.ORDER_ISSUE,
        initiator_role=ParticipantRole.CUSTOMER,
        target_role=ParticipantRole.PRODUCER,
        initial_message="Tive um problema com o meu pedido."
    )
    
    assert conversa.status == ConversationStatus.OPEN
    assert len(conversa.messages) == 1
    assert conversa.messages[0].content == "Tive um problema com o meu pedido."

def test_deve_enviar_mensagem_para_conversa_existente():
    repo = FakeCommunicationRepository()
    start_uc = StartConversationUseCase(repo)
    send_uc = SendMessageUseCase(repo)
    
    produtor_id = uuid.uuid4()
    conversa = start_uc.execute(
        initiator_id=uuid.uuid4(), target_id=produtor_id,
        subject_type=SubjectType.PRODUCT_QUESTION,
        initiator_role=ParticipantRole.CUSTOMER,
        target_role=ParticipantRole.PRODUCER,
        initial_message="O queijo é curado?"
    )
    
    # Produtor Responde
    conversa_atualizada = send_uc.execute(
        conversation_id=conversa.id,
        sender_id=produtor_id,
        sender_role=ParticipantRole.PRODUCER,
        content="Sim, tem 30 dias de cura!"
    )
    
    assert len(conversa_atualizada.messages) == 2
    assert conversa_atualizada.messages[1].content == "Sim, tem 30 dias de cura!"

def test_deve_fechar_conversa():
    repo = FakeCommunicationRepository()
    conversa = Conversation(
        initiator_id=uuid.uuid4(), target_id=uuid.uuid4(), 
        subject_type=SubjectType.SUPPORT_TICKET
    )
    repo.save(conversa)
    
    use_case = CloseConversationUseCase(repo)
    conversa_fechada = use_case.execute(conversa.id)
    
    assert conversa_fechada.status == ConversationStatus.CLOSED