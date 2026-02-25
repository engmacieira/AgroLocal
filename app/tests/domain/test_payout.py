import pytest
import uuid
from decimal import Decimal
from datetime import datetime, timezone
from app.domain.entities.order import Order, OrderStatus, DeliveryType
from app.domain.entities.payout import Payout, PayoutStatus

def test_deve_calcular_valores_de_repasse_corretamente():
    # Simulamos uma venda de R$ 100,00 com taxa de R$ 10,00
    repasse = Payout(
        order_id=uuid.uuid4(),
        producer_id=uuid.uuid4(),
        target_pix_key_snapshot="pix@produtor.com",
        amount_gross=Decimal("100.00"),
        amount_fee=Decimal("10.00")
    )
    
    # A entidade deve ter calculado o Net automaticamente: 100 - 10 = 90
    assert repasse.amount_net == Decimal("90.00")
    assert repasse.status == PayoutStatus.SCHEDULED
    assert repasse.scheduled_for is not None

def test_nao_deve_aceitar_taxa_maior_que_valor_bruto():
    with pytest.raises(ValueError, match="A taxa da plataforma não pode ser maior que o valor bruto"):
        Payout(
            order_id=uuid.uuid4(),
            producer_id=uuid.uuid4(),
            target_pix_key_snapshot="pix@produtor.com",
            amount_gross=Decimal("50.00"),
            amount_fee=Decimal("60.00") # Taxa maior que a venda!
        )

def test_deve_marcar_payout_como_pago_e_registrar_comprovante():
    repasse = Payout(
        order_id=uuid.uuid4(), producer_id=uuid.uuid4(),
        target_pix_key_snapshot="pix@produtor.com",
        amount_gross=Decimal("100.00"), amount_fee=Decimal("15.00")
    )
    
    # Simula o Admin a confirmar o pagamento
    repasse.mark_as_paid(bank_transaction_id="E2E-12345", proof_url="http://s3.com/recibo.pdf")
    
    assert repasse.status == PayoutStatus.PAID
    assert repasse.bank_transaction_id == "E2E-12345"
    assert repasse.proof_url == "http://s3.com/recibo.pdf"
    assert repasse.processed_at is not None

def test_falha_deve_exigir_motivo():
    repasse = Payout(
        order_id=uuid.uuid4(), producer_id=uuid.uuid4(),
        target_pix_key_snapshot="pix@produtor.com",
        amount_gross=Decimal("100.00"), amount_fee=Decimal("10.00")
    )
    
    with pytest.raises(ValueError, match="Motivo da falha é obrigatório"):
        repasse.mark_as_failed(reason="")
        
    repasse.mark_as_failed(reason="Chave PIX Inexistente")
    assert repasse.status == PayoutStatus.FAILED
    assert repasse.failure_reason == "Chave PIX Inexistente"

def test_ordem_deve_ter_status_completed_ao_finalizar():
    pedido = Order(customer_id=uuid.uuid4(), producer_id=uuid.uuid4(), delivery_type=DeliveryType.DOMICILIO, total_amount=Decimal("100.00"))
    
    # Simulando o avanço rápido da máquina de estados para poupar tempo no teste
    pedido.status = OrderStatus.DELIVERED 
    
    # Ação: O pagamento foi feito, marca o pedido como finalizado
    pedido.mark_as_completed()
    
    assert pedido.status == OrderStatus.COMPLETED # O novo status!