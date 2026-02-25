import pytest
import uuid
from app.domain.entities.catalog import Category, GlobalProduct, ProductStatus
from app.infrastructure.repositories.catalog_repository_impl import CategoryRepositoryImpl, GlobalProductRepositoryImpl

def test_deve_salvar_e_buscar_categoria(db_session):
    repo = CategoryRepositoryImpl(db_session)
    
    categoria = Category(name="Hortaliças", slug="hortalicas")
    repo.save(categoria)
    
    buscada = repo.get_by_slug("hortalicas")
    assert buscada is not None
    assert buscada.name == "Hortaliças"

def test_deve_salvar_produto_vinculado_a_categoria(db_session):
    # 1. Cria a Categoria (Obrigatório para a FK)
    cat_repo = CategoryRepositoryImpl(db_session)
    categoria = Category(name="Frutas", slug="frutas")
    cat_repo.save(categoria)
    
    # 2. Cria o Produto Global
    prod_repo = GlobalProductRepositoryImpl(db_session)
    produto = GlobalProduct(
        name="Laranja Pera",
        category_id=categoria.id,
        synonyms="laranja, laranja doce",
        ncm_code="08051000"
    )
    prod_repo.save(produto)
    
    # 3. Busca o produto
    salvo = prod_repo.get_by_name("Laranja Pera")
    assert salvo is not None
    assert salvo.status == ProductStatus.PENDING # Nasce pendente!
    assert salvo.ncm_code == "08051000"
    assert salvo.category_id == categoria.id

def test_deve_listar_produtos_aprovados_por_categoria(db_session):
    cat_repo = CategoryRepositoryImpl(db_session)
    prod_repo = GlobalProductRepositoryImpl(db_session)
    
    categoria = Category(name="Legumes", slug="legumes")
    cat_repo.save(categoria)
    
    prod1 = GlobalProduct(name="Cenoura", category_id=categoria.id)
    prod1.status = ProductStatus.APPROVED # Simulando aprovação
    
    prod2 = GlobalProduct(name="Batata", category_id=categoria.id)
    # Deixa a Batata como PENDING
    
    prod_repo.save(prod1)
    prod_repo.save(prod2)
    
    # Busca pela categoria (O repositório filtra apenas os APROVADOS)
    aprovados = prod_repo.get_by_category(categoria.id)
    
    assert len(aprovados) == 1
    assert aprovados[0].name == "Cenoura"