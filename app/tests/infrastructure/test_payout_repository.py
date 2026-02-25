import pytest
import uuid
from decimal import Decimal
from app.domain.entities.user import User
from app.domain.entities.order import Order, DeliveryType
from app.domain.entities.payout import Payout, PayoutStatus
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl
from app.infrastructure.repositories.payout_repository_impl import PayoutRepositoryImpl

def test_deve_salvar_e_recuperar_payout_corretamente(db_session):
    # 1. SETUP: Criar intervenientes e pedido
    user_repo = UserRepositoryImpl(db_session)
    cliente = user_repo.save(User(email="comprador_rep@teste.com", password_hash="12345678", full_name="C"))
    produtor = user_repo.save(User(email="produtor_rep@teste.com", password_hash="12345678", full_name="P"))
    
    order_repo = OrderRepositoryImpl(db_session)
    pedido = order_repo.save(Order(customer_id=cliente.id, producer_id=produtor.id, delivery_type=DeliveryType.RETIRADA_PRODUTOR, total_amount=Decimal("100.00")))
    
    # 2. ACTION: Criar e Salvar o Payout
    payout_repo = PayoutRepositoryImpl(db_session)
    repasse = Payout(
        order_id=pedido.id,
        producer_id=produtor.id,
        target_pix_key_snapshot="pix_do_produtor@banco.com",
        amount_gross=Decimal("100.00"),
        amount_fee=Decimal("10.00") # Taxa de 10%
    )
    payout_repo.save(repasse)
    
    # 3. ASSERT: Recuperar do banco e validar
    repasse_salvo = payout_repo.get_by_order_id(pedido.id)
    
    assert repasse_salvo is not None
    assert repasse_salvo.amount_net == Decimal("90.00") # Confirmamos que o banco gravou o valor líquido calculado!
    assert repasse_salvo.status == PayoutStatus.SCHEDULED
    assert repasse_salvo.target_pix_key_snapshot == "pix_do_produtor@banco.com"