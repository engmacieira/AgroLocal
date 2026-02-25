from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.communication import Conversation, Message
from app.domain.repositories.communication_repository import ICommunicationRepository
from app.infrastructure.models.communication_model import ConversationModel, MessageModel

class CommunicationRepositoryImpl(ICommunicationRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def _to_domain(self, model: ConversationModel) -> Conversation:
        # Reconstrói a lista de mensagens garantindo a ordem cronológica
        domain_messages = []
        for msg_model in sorted(model.messages, key=lambda m: m.created_at):
            domain_messages.append(Message(
                id=msg_model.id,
                sender_id=msg_model.sender_id,
                sender_role=msg_model.sender_role,
                content=msg_model.content,
                created_at=msg_model.created_at
            ))

        return Conversation(
            id=model.id,
            initiator_id=model.initiator_id,
            target_id=model.target_id,
            subject_type=model.subject_type,
            reference_id=model.reference_id,
            target_role=model.target_role,
            status=model.status,
            messages=domain_messages,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def save(self, conversation: Conversation) -> Conversation:
        # Tenta buscar a conversa para fazer um Update, se não existir, cria uma Nova (Insert)
        conv_model = self.db.query(ConversationModel).filter(ConversationModel.id == conversation.id).first()
        
        if not conv_model:
            conv_model = ConversationModel(
                id=conversation.id, initiator_id=conversation.initiator_id,
                target_id=conversation.target_id, subject_type=conversation.subject_type,
                reference_id=conversation.reference_id, target_role=conversation.target_role,
                status=conversation.status, created_at=conversation.created_at,
                updated_at=conversation.updated_at
            )
            self.db.add(conv_model)
        else:
            conv_model.status = conversation.status
            conv_model.updated_at = conversation.updated_at
        
        # Sincroniza as mensagens (Apenas adiciona as novas, pois mensagens antigas não mudam)
        existing_msg_ids = {m.id for m in conv_model.messages} if conv_model.messages else set()
        
        for domain_msg in conversation.messages:
            if domain_msg.id not in existing_msg_ids:
                new_msg_model = MessageModel(
                    id=domain_msg.id, conversation_id=conversation.id,
                    sender_id=domain_msg.sender_id, sender_role=domain_msg.sender_role,
                    content=domain_msg.content, created_at=domain_msg.created_at
                )
                self.db.add(new_msg_model)

        self.db.commit()
        return conversation

    def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        model = self.db.query(ConversationModel).filter(ConversationModel.id == conversation_id).first()
        return self._to_domain(model) if model else None

    def get_conversations_by_user(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Conversation]:
        models = self.db.query(ConversationModel).filter(
            (ConversationModel.initiator_id == user_id) | 
            (ConversationModel.target_id == user_id)
        ).order_by(ConversationModel.updated_at.desc()).offset(skip).limit(limit).all()
        
        return [self._to_domain(m) for m in models]