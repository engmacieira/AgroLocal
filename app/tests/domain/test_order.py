import pytest
import uuid
from decimal import Decimal
from app.domain.entities.order import Order, OrderItem, OrderStatus, DeliveryType

def test_deve_criar_pedido_e_calcular_totais_corretamente():
    customer_id = uuid.uuid4()
    producer_id = uuid.uuid4()
    
    # Cria o pedido base
    pedido = Order(
        customer_id=customer_id,
        producer_id=producer_id,
        delivery_type=DeliveryType.DOMICILIO,
        delivery_fee=Decimal("5.00") # Frete definido pela inteligência do carrinho
    )
    
    # Adiciona Itens (Snapshot do momento da compra)
    pedido.add_item(
        product_id=uuid.uuid4(),
        product_name_snapshot="Tomate Carmem",
        unit_snapshot="kg",
        unit_price_snapshot=Decimal("8.00"),
        quantity=2.0
    )
    pedido.add_item(
        product_id=uuid.uuid4(),
        product_name_snapshot="Alface Crespa",
        unit_snapshot="maço",
        unit_price_snapshot=Decimal("3.50"),
        quantity=1.0
    )
    
    # Verificações Matemáticas
    # Subtotal: (8 * 2) + (3.50 * 1) = 16.00 + 3.50 = 19.50
    # Total Final: 19.50 + Frete (5.00) = 24.50
    
    assert len(pedido.items) == 2
    assert pedido.items[0].subtotal == Decimal("16.00")
    assert pedido.items[1].subtotal == Decimal("3.50")
    assert pedido.total_amount == Decimal("24.50")
    assert pedido.status == OrderStatus.CREATED

def test_maquina_de_estados_fluxo_feliz():
    pedido = Order(
        customer_id=uuid.uuid4(), producer_id=uuid.uuid4(),
        delivery_type=DeliveryType.RETIRADA_PRODUTOR, total_amount=Decimal("10.00")
    )
    
    assert pedido.status == OrderStatus.CREATED
    
    pedido.mark_as_paid()
    assert pedido.status == OrderStatus.PAID
    
    pedido.start_preparing()
    assert pedido.status == OrderStatus.PREPARING
    
    pedido.mark_as_ready()
    assert pedido.status == OrderStatus.READY
    
    pedido.mark_as_delivered()
    assert pedido.status == OrderStatus.DELIVERED

def test_nao_deve_pular_etapas_da_maquina_de_estados():
    pedido = Order(
        customer_id=uuid.uuid4(), producer_id=uuid.uuid4(),
        delivery_type=DeliveryType.RETIRADA_PRODUTOR, total_amount=Decimal("10.00")
    )
    
    # Tenta marcar como entregue direto do CREATED
    with pytest.raises(ValueError, match="Transição de status inválida"):
        pedido.mark_as_delivered()

def test_cancelamento_deve_exigir_justificativa():
    pedido = Order(
        customer_id=uuid.uuid4(), producer_id=uuid.uuid4(),
        delivery_type=DeliveryType.RETIRADA_PRODUTOR, total_amount=Decimal("10.00")
    )
    
    with pytest.raises(ValueError, match="Justificativa é obrigatória para cancelamento"):
        pedido.cancel(reason="")
        
    pedido.cancel(reason="Produto sofreu avaria na colheita")
    assert pedido.status == OrderStatus.CANCELED
    assert pedido.cancellation_reason == "Produto sofreu avaria na colheita"