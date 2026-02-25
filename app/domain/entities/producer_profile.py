import uuid
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone

@dataclass(kw_only=True)
class ProducerProfile:
    """
    Entidade de Domínio: Perfil de Produtor.
    Contém as regras de negócio de quem vende na plataforma.
    """
    user_id: uuid.UUID
    store_name: str
    document: str  # Representa o CPF ou CNPJ
    pix_key: str
    
    # Vitrine (Opcionais)
    bio: Optional[str] = None
    cover_image: Optional[str] = None
    
    # Reputação (Regra de Negócio: Começa com 5.0 para incentivar vendas iniciais)
    rating: float = 5.0
    review_count: int = 0
    
    # Controlo
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_active: bool = True
    
    # Auditoria
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    # --- Comportamentos (Regras de Negócio) ---

    def update_details(self, new_name: Optional[str] = None, new_bio: Optional[str] = None, new_pix_key: Optional[str] = None) -> None:
        """Atualiza os dados públicos e financeiros do produtor."""
        if new_name:
            self.store_name = new_name
        if new_bio is not None:
            self.bio = new_bio
        if new_pix_key:
            self.pix_key = new_pix_key
            
        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        """Realiza o soft delete do perfil de produtor."""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)
        
    def add_review(self, new_rating: float) -> None:
        """Calcula a nova média de avaliações do produtor."""
        if not (1.0 <= new_rating <= 5.0):
            raise ValueError("A avaliação deve estar entre 1.0 e 5.0")
            
        # Fórmula de média ponderada simples
        total_score = (self.rating * self.review_count) + new_rating
        self.review_count += 1
        self.rating = round(total_score / self.review_count, 2)