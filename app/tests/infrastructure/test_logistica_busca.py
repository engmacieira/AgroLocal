import pytest
from decimal import Decimal
import uuid
from app.domain.entities.catalog import Category, GlobalProduct, ProductStatus
from app.domain.entities.producer_product import ProducerProduct, DeliveryOption, DeliveryType
from app.infrastructure.repositories.catalog_repository_impl import CategoryRepositoryImpl, GlobalProductRepositoryImpl
from app.infrastructure.repositories.producer_product_repository_impl import ProducerProductRepositoryImpl

def test_deve_buscar_produto_global_por_sinonimo(db_session):
    cat_repo = CategoryRepositoryImpl(db_session)
    prod_repo = GlobalProductRepositoryImpl(db_session)
    
    categoria = cat_repo.save(Category(name="Raízes Tubérculos", slug="raizes"))
    
    produto = GlobalProduct(
        name="Mandioca", 
        category_id=categoria.id,
        synonyms="macaxeira, aipim, castelinha"
    )
    produto.status = ProductStatus.APPROVED # Apenas aprovados aparecem na busca
    prod_repo.save(produto)
    
    # Busca pela palavra "macaxeira" (deve ignorar maiúsculas/minúsculas devido ao ilike)
    resultados = prod_repo.search_by_text("Macaxeira")
    
    assert len(resultados) == 1
    assert resultados[0].name == "Mandioca"

def test_deve_salvar_oferta_com_opcoes_de_entrega(db_session):
    # Simulamos UUIDs para não precisar criar a cadeia inteira de User/Produtor neste teste isolado
    offer_repo = ProducerProductRepositoryImpl(db_session)
    
    oferta = ProducerProduct(
        producer_id=uuid.uuid4(),
        global_product_id=uuid.uuid4(),
        price=Decimal("15.50")
    )
    
    oferta.set_delivery_options([
        DeliveryOption(delivery_type=DeliveryType.DOMICILIO, fee=Decimal("10.00"), schedule="Sábados"),
        DeliveryOption(delivery_type=DeliveryType.RETIRADA_PRODUTOR, fee=Decimal("0.00"), schedule="Diariamente")
    ])
    
    offer_repo.save(oferta)
    
    # Buscamos do banco para confirmar a gravação
    oferta_salva = offer_repo.get_by_id(oferta.id)
    
    assert oferta_salva is not None
    assert len(oferta_salva.delivery_options) == 2
    assert any(opt.delivery_type == DeliveryType.DOMICILIO and opt.fee == Decimal("10.00") for opt in oferta_salva.delivery_options)