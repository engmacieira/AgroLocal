import pytest
import uuid
from decimal import Decimal
from datetime import date
from app.domain.entities.producer_product import ProducerProduct, AvailabilityType, ProductImage, DeliveryType, DeliveryOption

def test_deve_criar_oferta_com_sucesso():
    oferta = ProducerProduct(
        producer_id=uuid.uuid4(),
        global_product_id=uuid.uuid4(),
        price=Decimal("12.50"), # Usamos Decimal para dinheiro!
        unit="kg",
        stock_quantity=50.0,
        availability_type=AvailabilityType.PRONTA_ENTREGA,
        harvest_date=date(2026, 2, 24)
    )

    assert oferta.price == Decimal("12.50")
    assert oferta.stock_quantity == 50.0
    assert oferta.is_active is True
    assert oferta.minimum_order_quantity == 1.0 # Valor default

def test_nao_deve_permitir_preco_zero_ou_negativo():
    with pytest.raises(ValueError, match="O preço da oferta deve ser maior que zero"):
        ProducerProduct(
            producer_id=uuid.uuid4(),
            global_product_id=uuid.uuid4(),
            price=Decimal("-5.00"),
            unit="kg",
            stock_quantity=10.0
        )

def test_nao_deve_permitir_quantidade_minima_invalida():
    with pytest.raises(ValueError, match="A quantidade mínima do pedido deve ser maior que zero"):
        ProducerProduct(
            producer_id=uuid.uuid4(),
            global_product_id=uuid.uuid4(),
            price=Decimal("10.00"),
            unit="kg",
            stock_quantity=10.0,
            minimum_order_quantity=0.0
        )

def test_deve_atualizar_estoque_com_sucesso():
    oferta = ProducerProduct(
        producer_id=uuid.uuid4(),
        global_product_id=uuid.uuid4(),
        price=Decimal("10.00"),
        unit="kg",
        stock_quantity=5.0
    )
    
    oferta.update_stock(add_quantity=15.5)
    assert oferta.stock_quantity == 20.5
    
    oferta.update_stock(add_quantity=-10.0)
    assert oferta.stock_quantity == 10.5

def test_nao_deve_permitir_estoque_ficar_negativo():
    oferta = ProducerProduct(
        producer_id=uuid.uuid4(),
        global_product_id=uuid.uuid4(),
        price=Decimal("10.00"),
        unit="kg",
        stock_quantity=5.0
    )
    
    with pytest.raises(ValueError, match="O estoque não pode ficar negativo"):
        oferta.update_stock(add_quantity=-10.0) # Tenta tirar mais do que tem

def test_deve_adicionar_imagem_a_oferta():
    oferta = ProducerProduct(
        producer_id=uuid.uuid4(),
        global_product_id=uuid.uuid4(),
        price=Decimal("10.00")
    )
    
    oferta.add_image(url="http://s3.aws.com/foto_tomate.jpg", is_primary=True)
    
    assert len(oferta.images) == 1
    assert oferta.images[0].url == "http://s3.aws.com/foto_tomate.jpg"
    assert oferta.images[0].is_primary is True
    
def test_deve_adicionar_opcoes_de_entrega_na_oferta():
    oferta = ProducerProduct(
        producer_id=uuid.uuid4(),
        global_product_id=uuid.uuid4(),
        price=Decimal("10.00")
    )
    
    # O produtor define duas formas de o cliente pegar o produto
    oferta.set_delivery_options([
        DeliveryOption(
            delivery_type=DeliveryType.DOMICILIO, 
            fee=Decimal("5.00"), 
            schedule="Sábados das 08h às 12h"
        ),
        DeliveryOption(
            delivery_type=DeliveryType.RETIRADA_PRODUTOR, 
            fee=Decimal("0.00"), 
            schedule="Segunda a Sexta"
        )
    ])
    
    assert len(oferta.delivery_options) == 2
    assert oferta.delivery_options[0].delivery_type == DeliveryType.DOMICILIO
    assert oferta.delivery_options[0].fee == Decimal("5.00")

def test_nao_deve_permitir_taxa_de_entrega_negativa():
    with pytest.raises(ValueError, match="A taxa de entrega não pode ser negativa"):
        DeliveryOption(
            delivery_type=DeliveryType.DOMICILIO, 
            fee=Decimal("-2.00") # Taxa negativa!
        )