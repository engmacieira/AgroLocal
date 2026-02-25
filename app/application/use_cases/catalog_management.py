import uuid
from typing import List, Optional
from dataclasses import dataclass
import re
from app.domain.entities.catalog import Category, GlobalProduct, ProductStatus
from app.domain.repositories.catalog_repository import ICategoryRepository, IGlobalProductRepository

class CreateCategoryUseCase:
    """Caso de Uso: Regista uma nova categoria base (Normalmente pelo Admin)."""
    def __init__(self, category_repository: ICategoryRepository):
        self.category_repository = category_repository

    def _generate_slug(self, name: str) -> str:
        """Gera uma URL amigável a partir do nome (Ex: 'Maçã Fuji' -> 'maca-fuji')."""
        import unicodedata
        # Remove acentos
        slug = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
        # Troca espaços por hifens e remove caracteres especiais
        slug = re.sub(r'[^\w\s-]', '', slug).strip().lower()
        slug = re.sub(r'[-\s]+', '-', slug)
        return slug

    def execute(self, name: str, icon_url: Optional[str] = None) -> Category:
        slug = self._generate_slug(name)
        
        if self.category_repository.get_by_slug(slug):
            raise ValueError("Já existe uma categoria com este nome ou slug similar")
            
        categoria = Category(name=name, slug=slug, icon_url=icon_url)
        return self.category_repository.save(categoria)

@dataclass
class SuggestProductDTO:
    name: str
    category_id: uuid.UUID
    suggested_by_id: Optional[uuid.UUID] = None
    synonyms: Optional[str] = None
    ncm_code: Optional[str] = None

class SuggestProductUseCase:
    """Caso de Uso: Um produtor ou Admin sugere um novo item para o catálogo."""
    def __init__(self, product_repository: IGlobalProductRepository, category_repository: ICategoryRepository):
        self.product_repository = product_repository
        self.category_repository = category_repository

    def execute(self, dto: SuggestProductDTO) -> GlobalProduct:
        # 1. Verifica se a categoria existe
        if not self.category_repository.get_by_id(dto.category_id):
            raise ValueError("Categoria informada não existe")

        # 2. Verifica duplicidade (nome exato)
        if self.product_repository.get_by_name(dto.name):
            raise ValueError("Já existe um produto com este nome no catálogo")

        novo_produto = GlobalProduct(
            name=dto.name,
            category_id=dto.category_id,
            suggested_by_id=dto.suggested_by_id,
            synonyms=dto.synonyms,
            ncm_code=dto.ncm_code
        )
        return self.product_repository.save(novo_produto)

class ApproveProductUseCase:
    """Caso de Uso: Admin aprova uma sugestão para a vitrine."""
    def __init__(self, product_repository: IGlobalProductRepository):
        self.product_repository = product_repository

    def execute(self, product_id: uuid.UUID, admin_id: uuid.UUID) -> GlobalProduct:
        produto = self.product_repository.get_by_id(product_id)
        if not produto:
            raise ValueError("Produto não encontrado")
            
        produto.approve(reviewer_id=admin_id)
        return self.product_repository.save(produto)

class RejectProductUseCase:
    """Caso de Uso: Admin rejeita uma sugestão (exige motivo)."""
    def __init__(self, product_repository: IGlobalProductRepository):
        self.product_repository = product_repository

    def execute(self, product_id: uuid.UUID, admin_id: uuid.UUID, reason: str) -> GlobalProduct:
        produto = self.product_repository.get_by_id(product_id)
        if not produto:
            raise ValueError("Produto não encontrado")
            
        produto.reject(reviewer_id=admin_id, reason=reason)
        return self.product_repository.save(produto)
    
class GetProductsByCategoryUseCase:
    """Caso de Uso: Produtor lista os produtos aprovados de uma categoria para vender."""
    def __init__(self, product_repository: IGlobalProductRepository):
        self.product_repository = product_repository

    def execute(self, category_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[GlobalProduct]:
        return self.product_repository.get_by_category(category_id, skip, limit)

class GetProductsByStatusUseCase:
    """Caso de Uso: Admin lista produtos por status (Ex: Fila de PENDING)."""
    def __init__(self, product_repository: IGlobalProductRepository):
        self.product_repository = product_repository

    def execute(self, status: ProductStatus, skip: int = 0, limit: int = 100) -> List[GlobalProduct]:
        return self.product_repository.get_all_by_status(status, skip, limit)