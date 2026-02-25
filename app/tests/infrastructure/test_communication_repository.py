import pytest
import uuid
from app.domain.entities.user import User
from app.domain.entities.communication import Conversation, SubjectType, ParticipantRole
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.communication_repository_impl import CommunicationRepositoryImpl

def test_deve_salvar_conversa_com_mensagens(db_session):
    # 1. SETUP: Criar utilizadores
    user_repo = UserRepositoryImpl(db_session)
    cliente = user_repo.save(User(email="cliente_chat@teste.com", password_hash="123", full_name="C"))
    produtor = user_repo.save(User(email="produtor_chat@teste.com", password_hash="123", full_name="P"))
    
    # 2. ACTION: Criar a Conversa e adicionar mensagens
    comm_repo = CommunicationRepositoryImpl(db_session)
    
    conversa = Conversation(
        initiator_id=cliente.id, target_id=produtor.id,
        subject_type=SubjectType.PRODUCT_QUESTION
    )
    # A primeira mensagem é criada em memória
    conversa.add_message(sender_id=cliente.id, sender_role=ParticipantRole.CUSTOMER, content="Boa tarde! O melão é doce?")
    
    # O Repositório guarda tudo de uma vez
    comm_repo.save(conversa)
    
    # 3. ACTION 2: Adicionar uma resposta e guardar novamente
    conversa_recuperada = comm_repo.get_by_id(conversa.id)
    conversa_recuperada.add_message(sender_id=produtor.id, sender_role=ParticipantRole.PRODUCER, content="Muito doce!")
    comm_repo.save(conversa_recuperada)
    
    # 4. ASSERT: Validar se a base de dados tem as duas tabelas perfeitamente alinhadas
    conversa_final = comm_repo.get_by_id(conversa.id)
    assert conversa_final is not None
    assert len(conversa_final.messages) == 2
    assert conversa_final.messages[0].content == "Boa tarde! O melão é doce?"
    assert conversa_final.messages[1].content == "Muito doce!"
    
    # Verifica vitrine de conversas do utilizador
    conversas_do_cliente = comm_repo.get_conversations_by_user(cliente.id)
    assert len(conversas_do_cliente) == 1
    assert conversas_do_cliente[0].id == conversa_final.id