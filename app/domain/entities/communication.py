import enum
import uuid
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime, timezone

class SubjectType(str, enum.Enum):
    """Categorias estruturadas para facilitar a triagem de chamados."""
    PRODUCT_QUESTION = "PRODUCT_QUESTION"   # Dúvida Sobre Produto
    DELIVERY_QUESTION = "DELIVERY_QUESTION" # Dúvida Sobre Entrega
    PRODUCER_QUESTION = "PRODUCER_QUESTION" # Dúvidas Direto com o Fornecedor
    ORDER_ISSUE = "ORDER_ISSUE"             # Dúvida Sobre Ordem Específica
    SUPPORT_TICKET = "SUPPORT_TICKET"       # Chamado Técnico (Problemas na Plataforma)

class ParticipantRole(str, enum.Enum):
    """Garante a auditoria e as permissões de quem está a falar."""
    CUSTOMER = "CUSTOMER"
    PRODUCER = "PRODUCER"
    ADMIN = "ADMIN"

class ConversationStatus(str, enum.Enum):
    """O ciclo de vida do chamado."""
    OPEN = "OPEN"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

@dataclass(kw_only=True)
class Message:
    """A mensagem individual (Imutável)."""
    sender_id: uuid.UUID
    sender_role: ParticipantRole
    content: str
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        """Validação de negócio da mensagem."""
        if not self.content or not str(self.content).strip():
            raise ValueError("A mensagem não pode estar vazia")
        self.content = str(self.content).strip()

@dataclass(kw_only=True)
class Conversation:
    """O Tópico/Chamado (O Agregador que controla as mensagens)."""
    initiator_id: uuid.UUID
    target_id: uuid.UUID
    subject_type: SubjectType
    reference_id: Optional[uuid.UUID] = None
    target_role: ParticipantRole = ParticipantRole.PRODUCER # Assumimos Produtor por defeito
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    status: ConversationStatus = ConversationStatus.OPEN
    messages: List[Message] = field(default_factory=list) # Relação com as mensagens
    
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        """Regras de criação do chamado."""
        # Evita que a plataforma vire uma "rede social" sem moderação
        if self.target_role == ParticipantRole.CUSTOMER:
            raise ValueError("Clientes não podem iniciar conversas com outros clientes")

    # --- Comportamentos ---

    def add_message(self, sender_id: uuid.UUID, sender_role: ParticipantRole, content: str) -> Message:
        """Adiciona uma mensagem garantindo que o chamado ainda está aberto."""
        if self.status == ConversationStatus.CLOSED:
            raise ValueError("Não é possível adicionar mensagens a uma conversa fechada")
            
        nova_mensagem = Message(
            sender_id=sender_id,
            sender_role=sender_role,
            content=content
        )
        self.messages.append(nova_mensagem)
        self.updated_at = datetime.now(timezone.utc)
        return nova_mensagem

    def resolve_conversation(self) -> None:
        """Marca o assunto como resolvido, mas ainda pode ser reaberto se necessário."""
        self.status = ConversationStatus.RESOLVED
        self.updated_at = datetime.now(timezone.utc)

    def close_conversation(self) -> None:
        """Tranca a conversa permanentemente (Somente leitura para auditoria)."""
        self.status = ConversationStatus.CLOSED
        self.updated_at = datetime.now(timezone.utc)