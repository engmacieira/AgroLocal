import pytest
import uuid
from typing import List, Optional
from app.domain.entities.catalog import Category, GlobalProduct, ProductStatus
from app.domain.repositories.catalog_repository import ICategoryRepository, IGlobalProductRepository
from app.application.use_cases.catalog_management import (
    CreateCategoryUseCase, SuggestProductUseCase, SuggestProductDTO,
    ApproveProductUseCase, RejectProductUseCase
)

# 1. Os Dublês de Testes (Fake Repositories)
class FakeCategoryRepository(ICategoryRepository):
    def __init__(self):
        self.categories: List[Category] = []

    def save(self, category: Category) -> Category:
        existing = self.get_by_id(category.id)
        if existing: self.categories.remove(existing)
        self.categories.append(category)
        return category

    def get_by_id(self, category_id: uuid.UUID) -> Optional[Category]:
        return next((c for c in self.categories if c.id == category_id), None)

    def get_by_slug(self, slug: str) -> Optional[Category]:
        return next((c for c in self.categories if c.slug == slug), None)

    def get_all_active(self) -> List[Category]:
        return [c for c in self.categories if c.is_active]

class FakeGlobalProductRepository(IGlobalProductRepository):
    def __init__(self):
        self.products: List[GlobalProduct] = []

    def save(self, product: GlobalProduct) -> GlobalProduct:
        existing = self.get_by_id(product.id)
        if existing: self.products.remove(existing)
        self.products.append(product)
        return product

    def get_by_id(self, product_id: uuid.UUID) -> Optional[GlobalProduct]:
        return next((p for p in self.products if p.id == product_id), None)

    def get_by_name(self, name: str) -> Optional[GlobalProduct]:
        return next((p for p in self.products if p.name == name), None)

    def get_all_by_status(self, status: ProductStatus, skip: int = 0, limit: int = 100) -> List[GlobalProduct]:
        filtrados = [p for p in self.products if p.status == status]
        return filtrados[skip : skip + limit]

    def get_by_category(self, category_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[GlobalProduct]:
        filtrados = [p for p in self.products if p.category_id == category_id and p.status == ProductStatus.APPROVED]
        return filtrados[skip : skip + limit]

# 2. Testes dos Casos de Uso

def test_deve_criar_categoria_com_slug_gerado_automaticamente():
    fake_repo = FakeCategoryRepository()
    use_case = CreateCategoryUseCase(fake_repo)
    
    # Repare: Nós não passamos o slug, o Caso de Uso deve gerá-lo!
    categoria = use_case.execute(name="Frutas Vermelhas")
    
    assert categoria.name == "Frutas Vermelhas"
    assert categoria.slug == "frutas-vermelhas"

def test_deve_sugerir_novo_produto_global():
    cat_repo = FakeCategoryRepository()
    prod_repo = FakeGlobalProductRepository()
    
    categoria = cat_repo.save(Category(name="Laticínios", slug="laticinios"))
    
    use_case = SuggestProductUseCase(prod_repo, cat_repo)
    dto = SuggestProductDTO(
        name="Queijo Minas Padrão",
        category_id=categoria.id,
        suggested_by_id=uuid.uuid4()
    )
    
    produto = use_case.execute(dto)
    
    assert produto.name == "Queijo Minas Padrão"
    assert produto.status == ProductStatus.PENDING

def test_nao_deve_permitir_produto_com_nome_duplicado():
    prod_repo = FakeGlobalProductRepository()
    cat_repo = FakeCategoryRepository()
    categoria = cat_repo.save(Category(name="Legumes", slug="legumes"))
    
    # Criamos o primeiro
    prod_repo.save(GlobalProduct(name="Cenoura", category_id=categoria.id))
    
    use_case = SuggestProductUseCase(prod_repo, cat_repo)
    
    with pytest.raises(ValueError, match="Já existe um produto com este nome no catálogo"):
        use_case.execute(SuggestProductDTO(name="Cenoura", category_id=categoria.id))

def test_admin_deve_aprovar_produto():
    prod_repo = FakeGlobalProductRepository()
    produto = prod_repo.save(GlobalProduct(name="Milho", category_id=uuid.uuid4()))
    admin_id = uuid.uuid4()
    
    use_case = ApproveProductUseCase(prod_repo)
    use_case.execute(product_id=produto.id, admin_id=admin_id)
    
    assert produto.status == ProductStatus.APPROVED
    assert produto.reviewed_by_id == admin_id

def test_admin_deve_rejeitar_produto_com_motivo():
    prod_repo = FakeGlobalProductRepository()
    produto = prod_repo.save(GlobalProduct(name="Tomate Estregado", category_id=uuid.uuid4()))
    
    use_case = RejectProductUseCase(prod_repo)
    use_case.execute(product_id=produto.id, admin_id=uuid.uuid4(), reason="Nome inválido/Ofensivo")
    
    assert produto.status == ProductStatus.REJECTED