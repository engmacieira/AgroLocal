from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.catalog import Category, GlobalProduct, ProductStatus

class ICategoryRepository(ABC):
    @abstractmethod
    def save(self, category: Category) -> Category:
        pass

    @abstractmethod
    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        pass
        
    @abstractmethod
    def get_by_slug(self, slug: str) -> Optional[Category]:
        pass

    @abstractmethod
    def get_all_active(self) -> List[Category]:
        pass

class IGlobalProductRepository(ABC):
    @abstractmethod
    def save(self, product: GlobalProduct) -> GlobalProduct:
        pass

    @abstractmethod
    def get_by_id(self, product_id: UUID) -> Optional[GlobalProduct]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[GlobalProduct]:
        """Busca exata pelo nome para evitar duplicidade."""
        pass

    @abstractmethod
    def get_all_by_status(self, status: ProductStatus, skip: int = 0, limit: int = 100) -> List[GlobalProduct]:
        """Busca produtos por status (Ex: PENDING para a fila de curadoria do Admin)."""
        pass
        
    @abstractmethod
    def get_by_category(self, category_id: UUID, skip: int = 0, limit: int = 100) -> List[GlobalProduct]:
        """Lista os produtos aprovados de uma categoria específica."""
        pass
    
    @abstractmethod
    def search_by_text(self, query: str, skip: int = 0, limit: int = 100) -> List[GlobalProduct]:
        """Busca textual no nome e nos sinônimos (Apenas APROVADOS)."""
        pass