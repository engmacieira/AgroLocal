from pydantic import Field, ConfigDict, AnyHttpUrl
from typing import Optional, List
from uuid import UUID
from decimal import Decimal
from datetime import date
from app.models.product_model import AvailabilityType
from app.schemas.base_schema import BaseSchema, TimestampSchema
from app.schemas.catalog_schema import GlobalProductRead

# --- Imagens do Produto ---

class ProductImageBase(BaseSchema):
    """
    Schema para fotos reais do produto ofertado.
    """
    url: str = Field(
        ..., 
        description="URL pública da imagem (S3, Firebase, etc)",
        examples=["https://bucket.agrolocal.com/tomate-1.jpg"]
    )
    
    is_primary: bool = Field(
        default=False,
        description="Define se esta é a foto de capa da oferta (aparece na listagem)"
    )

class ProductImageRead(ProductImageBase):
    id: UUID = Field(description="ID único da imagem")

# --- Oferta do Produtor ---

class ProducerProductBase(BaseSchema):
    """
    Schema base para a Oferta (Vínculo entre Produtor e Produto Global).
    Define as condições de venda (Preço, Estoque, Frescor).
    """
    global_product_id: UUID = Field(
        ..., 
        description="ID do produto no Catálogo Mestre (O que você está vendendo?)"
    )
    
    price: Decimal = Field(
        ..., 
        gt=0, 
        decimal_places=2,
        description="Preço de venda por unidade (R$)",
        examples=[5.50, 12.00]
    )
    
    unit: str = Field(
        default="kg", 
        max_length=20,
        description="Unidade de medida (kg, maço, dúzia, unidade)",
        examples=["kg", "maço", "bandeja 500g"]
    )
    
    stock_quantity: float = Field(
        default=0.0,
        ge=0,
        description="Quantidade disponível em estoque"
    )
    
    availability_type: AvailabilityType = Field(
        default=AvailabilityType.PRONTA_ENTREGA,
        description="Logística: O produto já está colhido ou será colhido sob demanda?"
    )
    
    minimum_order_quantity: float = Field(
        default=1.0,
        gt=0,
        description="Quantidade mínima para compra (Ex: Vender no mínimo 2kg)"
    )
    
    description: Optional[str] = Field(
        default=None, 
        max_length=1000,
        description="Detalhes sobre a qualidade, cultivo ou frescor do lote",
        examples=["Tomates colhidos hoje pela manhã. Sem agrotóxicos."]
    )
    
    harvest_date: Optional[date] = Field(
        default=None,
        description="Data da colheita (Vital para perecíveis)",
        examples=["2026-02-18"]
    )
    
    is_active: bool = Field(
        default=True,
        description="Se falso, o produto fica oculto no App (Pausado)"
    )

class ProducerProductCreate(ProducerProductBase):
    """
    Payload para criar uma nova oferta.
    Permite enviar imagens já no momento da criação.
    """
    images: Optional[List[ProductImageBase]] = Field(
        default=None,
        description="Lista de fotos do produto (Opcional na criação)"
    )

    # Exemplo Rico para o Swagger
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "global_product_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                    "price": 8.50,
                    "unit": "kg",
                    "stock_quantity": 100.0,
                    "availability_type": "PRONTA_ENTREGA",
                    "minimum_order_quantity": 1.0,
                    "description": "Tomates orgânicos muito doces, safra especial.",
                    "harvest_date": "2026-02-18",
                    "images": [
                        {
                            "url": "https://storage.com/img1.jpg",
                            "is_primary": True
                        }
                    ]
                }
            ]
        }
    )

class ProducerProductRead(ProducerProductBase, TimestampSchema):
    """
    Visualização da oferta para o Consumidor.
    """
    id: UUID = Field(description="ID único da oferta")
    
    producer_id: UUID = Field(description="ID do produtor que está vendendo")
    
    # Nested Object: Trazemos os dados do catálogo (Nome, Foto padrão) automaticamente
    global_info: GlobalProductRead = Field(
        description="Detalhes do produto original do catálogo (Nome, Categoria, etc)"
    )
    
    images: List[ProductImageRead] = Field(
        default=[],
        description="Galeria de fotos reais enviadas pelo produtor"
    )