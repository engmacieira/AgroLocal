import pytest
import uuid
from decimal import Decimal
from app.domain.entities.user import User
from app.domain.entities.order import Order, DeliveryType
from app.domain.entities.review import Review
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl
from app.infrastructure.repositories.review_repository_impl import ReviewRepositoryImpl

def test_deve_salvar_e_recuperar_avaliacao(db_session):
    # 1. SETUP: Criar utilizadores e Pedido
    user_repo = UserRepositoryImpl(db_session)
    cliente = user_repo.save(User(email="avaliador@teste.com", password_hash="12345678", full_name="A"))
    produtor = user_repo.save(User(email="avaliado@teste.com", password_hash="12345678", full_name="P"))
    
    order_repo = OrderRepositoryImpl(db_session)
    pedido = order_repo.save(Order(customer_id=cliente.id, producer_id=produtor.id, delivery_type=DeliveryType.DOMICILIO, total_amount=Decimal("30.00")))
    
    # 2. ACTION: Criar e salvar Review
    review_repo = ReviewRepositoryImpl(db_session)
    avaliacao = Review(
        order_id=pedido.id,
        customer_id=cliente.id,
        producer_id=produtor.id,
        rating=5,
        comment="Excelente!",
        photo_url="http://s3.com/foto.jpg"
    )
    review_repo.save(avaliacao)
    
    # 3. ASSERT: Validar recuperação e relacionamento
    salvo = review_repo.get_by_order_id(pedido.id)
    assert salvo is not None
    assert salvo.rating == 5
    assert salvo.comment == "Excelente!"
    assert salvo.photo_url == "http://s3.com/foto.jpg"

    # Vitrine do produtor
    vitrine = review_repo.get_by_producer_id(produtor.id)
    assert len(vitrine) == 1
    assert vitrine[0].id == avaliacao.id