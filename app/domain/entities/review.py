import uuid
from dataclasses import dataclass, field
from typing import Optional
from datetime import datetime, timezone

@dataclass(kw_only=True)
class Review:
    """
    Entidade de Avaliação (Review).
    Representa a Prova Social e Reputação de um produtor na plataforma.
    Garante o vínculo 1:1 com uma Ordem de Compra Verificada.
    """
    order_id: uuid.UUID
    customer_id: uuid.UUID
    producer_id: uuid.UUID
    rating: int
    
    comment: Optional[str] = None
    photo_url: Optional[str] = None
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self):
        """Aplica as regras de negócio de reputação."""
        
        # 1. Validação da Nota (Rating)
        if type(self.rating) is not int or self.rating < 1 or self.rating > 5:
            raise ValueError("A nota deve ser um número inteiro entre 1 e 5")
            
        # 2. Higienização do Comentário (Limpa espaços e anula se ficar vazio)
        if self.comment is not None:
            cleaned_comment = self.comment.strip()
            self.comment = cleaned_comment if cleaned_comment else None
            
        # 3. Higienização da URL da Foto
        if self.photo_url is not None:
            cleaned_url = self.photo_url.strip()
            self.photo_url = cleaned_url if cleaned_url else None