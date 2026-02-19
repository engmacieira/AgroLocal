from pydantic import Field, ConfigDict
from typing import Optional
from uuid import UUID
from app.schemas.base_schema import BaseSchema, TimestampSchema

class ReviewBase(BaseSchema):
    """
    Schema base para Avaliações (Reviews).
    O sistema de reputação é baseado em compras verificadas (Verified Purchase),
    exigindo o vínculo com um Pedido.
    """
    order_id: UUID = Field(
        ..., 
        description="ID do pedido que está sendo avaliado (Prova de compra)"
    )
    
    producer_id: UUID = Field(
        ..., 
        description="ID do produtor que está recebendo a nota"
    )
    
    rating: int = Field(
        ..., 
        ge=1, 
        le=5, 
        description="Nota de satisfação de 1 (Péssimo) a 5 (Excelente)",
        examples=[5]
    )
    
    comment: Optional[str] = Field(
        default=None, 
        max_length=500, 
        description="Opinião textual sobre a qualidade dos produtos e serviço",
        examples=["Produtos muito frescos, chegaram antes do prazo!"]
    )

class ReviewCreate(ReviewBase):
    """
    Payload para submeter uma nova avaliação.
    """
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "order_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                    "producer_id": "b2f4c810-1d2a-4f5b-9c8e-2a3b4c5d6e7f",
                    "rating": 5,
                    "comment": "Adorei os tomates, virei freguês!"
                }
            ]
        }
    )

class ReviewRead(ReviewBase, TimestampSchema):
    """
    Exibição pública da avaliação na vitrine do produtor.
    """
    id: UUID = Field(description="ID único da avaliação")
    
    author_id: UUID = Field(
        description="ID do cliente que escreveu a avaliação"
    )