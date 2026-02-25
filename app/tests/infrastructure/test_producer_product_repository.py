import pytest
from decimal import Decimal
from app.domain.entities.user import User
from app.domain.entities.producer_profile import ProducerProfile
from app.domain.entities.catalog import Category, GlobalProduct, ProductStatus
from app.domain.entities.producer_product import ProducerProduct
from app.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from app.infrastructure.repositories.producer_repository_impl import ProducerRepositoryImpl
from app.infrastructure.repositories.catalog_repository_impl import CategoryRepositoryImpl, GlobalProductRepositoryImpl
from app.infrastructure.repositories.producer_product_repository_impl import ProducerProductRepositoryImpl

def test_deve_salvar_e_buscar_oferta_com_imagens(db_session):
    # --- ARRANGE: PREPARANDO O TERRENO ---
    # 1. Cria User e Produtor
    user_repo = UserRepositoryImpl(db_session)
    user = user_repo.save(User(email="sitio@teste.com", password_hash="123", full_name="Sitio"))
    
    prod_repo = ProducerRepositoryImpl(db_session)
    produtor = prod_repo.save(ProducerProfile(user_id=user.id, store_name="Sitio", document="000", pix_key="000"))
    
    # 2. Cria Categoria e Produto Global
    cat_repo = CategoryRepositoryImpl(db_session)
    categoria = cat_repo.save(Category(name="Raizes", slug="raizes"))
    
    global_repo = GlobalProductRepositoryImpl(db_session)
    produto_global = global_repo.save(GlobalProduct(name="Mandioca", category_id=categoria.id))
    
    # --- ACT: SALVANDO A OFERTA ---
    offer_repo = ProducerProductRepositoryImpl(db_session)
    oferta = ProducerProduct(
        producer_id=produtor.id,
        global_product_id=produto_global.id,
        price=Decimal("4.50"),
        unit="kg",
        stock_quantity=100.0
    )
    # Adicionando uma imagem
    oferta.add_image(url="http://s3.com/mandioca.jpg", is_primary=True)
    
    offer_repo.save(oferta)
    
    # --- ASSERT: BUSCANDO A OFERTA ---
    oferta_salva = offer_repo.get_by_id(oferta.id)
    
    assert oferta_salva is not None
    assert oferta_salva.price == Decimal("4.50")
    assert oferta_salva.stock_quantity == 100.0
    assert len(oferta_salva.images) == 1
    assert oferta_salva.images[0].url == "http://s3.com/mandioca.jpg"