import pytest
import uuid
from decimal import Decimal
from app.domain.entities.user import User
from app.domain.entities.order import Order, DeliveryType
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl

def test_deve_salvar_e_recuperar_pedido_com_itens(db_session):
    # 1. Preparação (Criamos 2 utilizadores para serem cliente e produtor)
    user_repo = UserRepositoryImpl(db_session)
    cliente = user_repo.save(User(email="cliente@teste.com", password_hash="123", full_name="Cliente"))
    produtor = user_repo.save(User(email="vendedor@teste.com", password_hash="123", full_name="Produtor"))
    
    # 2. Ação (Criamos o pedido no Domínio)
    order_repo = OrderRepositoryImpl(db_session)
    
    pedido = Order(
        customer_id=cliente.id,
        producer_id=produtor.id,
        delivery_type=DeliveryType.RETIRADA_PRODUTOR,
        delivery_fee=Decimal("0.00")
    )
    
    pedido.add_item(
        product_id=uuid.uuid4(), # Pode ser um UUID fantasma para o teste
        product_name_snapshot="Cebola Orgânica",
        unit_snapshot="kg",
        unit_price_snapshot=Decimal("6.50"),
        quantity=2.0
    )
    
    pedido_salvo = order_repo.save(pedido)
    
    # 3. Verificação (Lemos do banco)
    pedido_recuperado = order_repo.get_by_id(pedido_salvo.id)
    
    assert pedido_recuperado is not None
    assert pedido_recuperado.total_amount == Decimal("13.00")
    assert len(pedido_recuperado.items) == 1
    assert pedido_recuperado.items[0].product_name_snapshot == "Cebola Orgânica"