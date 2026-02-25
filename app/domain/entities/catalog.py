import enum
import uuid
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone

class ProductStatus(str, enum.Enum):
    """Workflow de aprovação de novos itens no catálogo."""
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    ARCHIVED = "ARCHIVED"

@dataclass(kw_only=True)
class Category:
    """Entidade: Categoria de Produtos (Ex: Frutas, Laticínios)"""
    name: str
    slug: str
    icon_url: Optional[str] = None
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_active: bool = True

@dataclass(kw_only=True)
class GlobalProduct:
    """
    Entidade: Produto Global do Catálogo.
    A "Verdade" do sistema para evitar itens duplicados.
    """
    name: str
    category_id: uuid.UUID
    
    # Dados Opcionais e Busca
    scientific_name: Optional[str] = None
    synonyms: Optional[str] = None
    taxonomy_code: Optional[str] = None
    ncm_code: Optional[str] = None
    description_template: Optional[str] = None
    image_url: Optional[str] = None
    
    # Workflow e Moderação
    status: ProductStatus = ProductStatus.PENDING
    suggested_by_id: Optional[uuid.UUID] = None
    reviewed_by_id: Optional[uuid.UUID] = None
    rejection_reason: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    
    # Identificadores e Auditoria
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    # --- Comportamentos (Regras de Negócio) ---

    def approve(self, reviewer_id: uuid.UUID) -> None:
        """Aprova o produto para aparecer na listagem dos produtores."""
        self.status = ProductStatus.APPROVED
        self.reviewed_by_id = reviewer_id
        self.reviewed_at = datetime.now(timezone.utc)
        self.rejection_reason = None # Limpa caso tenha sido rejeitado antes

    def reject(self, reviewer_id: uuid.UUID, reason: str) -> None:
        """Rejeita a sugestão do produto (Exige um motivo)."""
        if not reason or not reason.strip():
            raise ValueError("Motivo da rejeição é obrigatório")
            
        self.status = ProductStatus.REJECTED
        self.reviewed_by_id = reviewer_id
        self.rejection_reason = reason.strip()
        self.reviewed_at = datetime.now(timezone.utc)

    def archive(self) -> None:
        """Tira o produto de linha (não apaga o histórico)."""
        self.status = ProductStatus.ARCHIVED