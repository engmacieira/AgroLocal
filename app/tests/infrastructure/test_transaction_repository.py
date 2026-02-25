import pytest
import uuid
from decimal import Decimal
from app.domain.entities.user import User
from app.domain.entities.order import Order, DeliveryType, OrderStatus
from app.domain.entities.transaction import Transaction, PaymentMethod, TransactionStatus
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl
from app.infrastructure.repositories.transaction_repository_impl import TransactionRepositoryImpl

def test_deve_salvar_transacao_e_vincular_pedidos(db_session):
    # 1. SETUP: Criar Usuários
    user_repo = UserRepositoryImpl(db_session)
    cliente = user_repo.save(User(email="comprador_pix@teste.com", password_hash="12345678", full_name="C"))
    produtor = user_repo.save(User(email="vendedor_pix@teste.com", password_hash="123456789", full_name="V"))
    
    # 2. SETUP: Criar 2 Pedidos
    order_repo = OrderRepositoryImpl(db_session)
    pedido1 = order_repo.save(Order(customer_id=cliente.id, producer_id=produtor.id, delivery_type=DeliveryType.RETIRADA_PRODUTOR, total_amount=Decimal("15.00")))
    pedido2 = order_repo.save(Order(customer_id=cliente.id, producer_id=produtor.id, delivery_type=DeliveryType.DOMICILIO, total_amount=Decimal("20.00")))

    # 3. ACTION: Criar Transação
    trans_repo = TransactionRepositoryImpl(db_session)
    transacao = Transaction(payment_method=PaymentMethod.PIX, orders=[pedido1, pedido2])
    
    # Simula o Webhook chegando e aprovando tudo!
    transacao.approve(external_id="STRIPE-999")
    trans_repo.save(transacao)

    # 4. ASSERT: Recupera do banco e valida a cascata
    trans_salva = trans_repo.get_by_id(transacao.id)
    
    assert trans_salva is not None
    assert trans_salva.amount == Decimal("35.00") # Somou corretamente (15 + 20)
    assert trans_salva.status == TransactionStatus.APPROVED
    assert len(trans_salva.orders) == 2
    
    # Verifica se os pedidos foram atualizados para PAID no banco
    pedido_banco = order_repo.get_by_id(pedido1.id)
    assert pedido_banco.status == OrderStatus.PAID