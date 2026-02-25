import pytest
import uuid
from app.domain.entities.communication import (
    Conversation, Message, SubjectType, ParticipantRole, ConversationStatus
)

def test_deve_criar_conversa_e_adicionar_mensagens():
    cliente_id = uuid.uuid4()
    produtor_id = uuid.uuid4()
    pedido_id = uuid.uuid4()

    # Cria o "Cabeçalho" (O Chamado/Tópico)
    conversa = Conversation(
        initiator_id=cliente_id,
        target_id=produtor_id,
        subject_type=SubjectType.ORDER_ISSUE,
        reference_id=pedido_id # Contexto: Estão a falar sobre este pedido
    )
    
    # Adiciona a primeira mensagem (Corpo)
    conversa.add_message(
        sender_id=cliente_id,
        sender_role=ParticipantRole.CUSTOMER,
        content="Olá, o meu pedido veio a faltar uma alface."
    )
    
    # Produtor responde
    conversa.add_message(
        sender_id=produtor_id,
        sender_role=ParticipantRole.PRODUCER,
        content="Peço desculpa! Vou enviar amanhã."
    )

    assert conversa.status == ConversationStatus.OPEN
    assert len(conversa.messages) == 2
    assert conversa.messages[0].content == "Olá, o meu pedido veio a faltar uma alface."

def test_nao_deve_permitir_cliente_iniciar_conversa_com_cliente():
    cliente_1_id = uuid.uuid4()
    cliente_2_id = uuid.uuid4()

    # Tenta criar uma conversa onde o alvo também é um cliente
    with pytest.raises(ValueError, match="Clientes não podem iniciar conversas com outros clientes"):
        Conversation(
            initiator_id=cliente_1_id,
            target_id=cliente_2_id,
            subject_type=SubjectType.PRODUCT_QUESTION,
            target_role=ParticipantRole.CUSTOMER # Identificamos o alvo como cliente
        )

def test_nao_deve_permitir_mensagem_vazia():
    conversa = Conversation(
        initiator_id=uuid.uuid4(), target_id=uuid.uuid4(),
        subject_type=SubjectType.SUPPORT_TICKET
    )
    
    with pytest.raises(ValueError, match="A mensagem não pode estar vazia"):
        conversa.add_message(sender_id=uuid.uuid4(), sender_role=ParticipantRole.CUSTOMER, content="   ")

def test_nao_deve_adicionar_mensagem_em_conversa_fechada():
    conversa = Conversation(
        initiator_id=uuid.uuid4(), target_id=uuid.uuid4(),
        subject_type=SubjectType.DELIVERY_QUESTION
    )
    
    # O Admin ou o utilizador fecha o chamado
    conversa.close_conversation()
    
    with pytest.raises(ValueError, match="Não é possível adicionar mensagens a uma conversa fechada"):
        conversa.add_message(
            sender_id=uuid.uuid4(),
            sender_role=ParticipantRole.PRODUCER,
            content="Ainda está aí?"
        )