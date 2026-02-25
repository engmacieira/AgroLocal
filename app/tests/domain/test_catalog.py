import pytest
import uuid
from app.domain.entities.catalog import Category, GlobalProduct, ProductStatus

def test_deve_criar_categoria_com_sucesso():
    categoria = Category(name="Frutas Cítricas", slug="frutas-citricas")
    
    assert categoria.name == "Frutas Cítricas"
    assert categoria.slug == "frutas-citricas"
    assert categoria.is_active is True

def test_deve_criar_produto_global_pendente():
    produto = GlobalProduct(
        name="Tomate Carmem",
        category_id=uuid.uuid4(),
        suggested_by_id=uuid.uuid4(),
        synonyms="tomate, tomate salada"
    )

    # Regra de Negócio: Todo produto sugerido nasce como PENDING
    assert produto.name == "Tomate Carmem"
    assert produto.status == ProductStatus.PENDING

def test_deve_aprovar_produto_global():
    produto = GlobalProduct(
        name="Alface Crespa",
        category_id=uuid.uuid4()
    )
    admin_id = uuid.uuid4()
    
    produto.approve(reviewer_id=admin_id)
    
    assert produto.status == ProductStatus.APPROVED
    assert produto.reviewed_by_id == admin_id
    assert produto.reviewed_at is not None

def test_nao_deve_rejeitar_produto_sem_motivo():
    produto = GlobalProduct(
        name="Produto Duplicado",
        category_id=uuid.uuid4()
    )
    admin_id = uuid.uuid4()
    
    # Regra de Negócio: Rejeição exige feedback
    with pytest.raises(ValueError, match="Motivo da rejeição é obrigatório"):
        produto.reject(reviewer_id=admin_id, reason="")
        
def test_deve_rejeitar_produto_com_motivo():
    produto = GlobalProduct(
        name="Produto Duplicado",
        category_id=uuid.uuid4()
    )
    admin_id = uuid.uuid4()
    
    produto.reject(reviewer_id=admin_id, reason="Já existe um produto com este nome")
    
    assert produto.status == ProductStatus.REJECTED
    assert produto.rejection_reason == "Já existe um produto com este nome"