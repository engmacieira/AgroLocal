import pytest
import uuid
from decimal import Decimal
from app.domain.entities.order import Order, OrderStatus, DeliveryType
from app.domain.entities.transaction import Transaction, TransactionStatus, PaymentMethod

def test_deve_criar_transacao_unificada_com_multiplos_pedidos():
    # Simulamos 2 pedidos diferentes saindo do mesmo carrinho
    pedido1 = Order(
        customer_id=uuid.uuid4(), producer_id=uuid.uuid4(),
        delivery_type=DeliveryType.RETIRADA_PRODUTOR, total_amount=Decimal("50.00")
    )
    pedido2 = Order(
        customer_id=uuid.uuid4(), producer_id=uuid.uuid4(),
        delivery_type=DeliveryType.DOMICILIO, total_amount=Decimal("35.50")
    )
    
    # Criamos a transação vinculando os pedidos
    transacao = Transaction(
        payment_method=PaymentMethod.PIX,
        orders=[pedido1, pedido2]
    )
    
    # Verificações
    assert transacao.amount == Decimal("85.50") # 50.00 + 35.50
    assert transacao.status == TransactionStatus.PENDING
    assert transacao.installments == 1

def test_deve_aprovar_transacao_e_marcar_pedidos_como_pagos():
    pedido = Order(
        customer_id=uuid.uuid4(), producer_id=uuid.uuid4(),
        delivery_type=DeliveryType.RETIRADA_PRODUTOR, total_amount=Decimal("100.00")
    )
    
    transacao = Transaction(payment_method=PaymentMethod.PIX, orders=[pedido])
    
    # Simula o Webhook do Gateway dizendo "Foi pago!"
    transacao.approve(external_id="PAY-12345")
    
    assert transacao.status == TransactionStatus.APPROVED
    assert transacao.external_transaction_id == "PAY-12345"
    assert pedido.status == OrderStatus.PAID # O pedido atualizou junto!