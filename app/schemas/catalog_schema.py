from pydantic import Field, ConfigDict
from typing import Optional
from uuid import UUID
from app.models.catalog_model import ProductStatus
from app.schemas.base_schema import BaseSchema, TimestampSchema

# --- Categorias ---

class CategoryBase(BaseSchema):
    """
    Schema base para Categorias de Produtos.
    Define a organização principal da navegação do App (Ex: Frutas, Legumes).
    """
    name: str = Field(
        ..., 
        min_length=2, 
        max_length=50,
        description="Nome visível da categoria",
        examples=["Legumes e Verduras"]
    )
    
    slug: str = Field(
        ..., 
        pattern=r"^[a-z0-9-]+$",
        max_length=50,
        description="Identificador amigável para URL (apenas letras minúsculas e hífen)",
        examples=["legumes-e-verduras"]
    )
    
    icon_url: Optional[str] = Field(
        default=None,
        description="URL de ícone ou Emoji representando a categoria",
        examples=["🥦", "https://cdn.agrolocal.com/icons/legumes.png"]
    )
    
    is_active: bool = Field(
        default=True,
        description="Define se a categoria aparece no App"
    )

class CategoryCreate(CategoryBase):
    """Payload para criar uma nova categoria via Painel Admin."""
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Frutas Cítricas",
                    "slug": "frutas-citricas",
                    "icon_url": "🍊",
                    "is_active": True
                }
            ]
        }
    )

class CategoryRead(CategoryBase):
    """Retorno de dados da categoria com ID."""
    id: UUID = Field(description="ID único da categoria")

# --- Produtos Globais ---

class GlobalProductBase(BaseSchema):
    """
    Schema do Catálogo Mestre.
    Estes são os 'templates' de produtos que os produtores escolhem para vender.
    """
    name: str = Field(
        ..., 
        min_length=3, 
        max_length=100,
        description="Nome oficial do produto (Padrão)",
        examples=["Mandioca de Mesa (Aipim)"]
    )
    
    scientific_name: Optional[str] = Field(
        default=None, 
        max_length=100,
        description="Nome científico (opcional, para catalogação técnica)",
        examples=["Manihot esculenta"]
    )
    
    synonyms: Optional[str] = Field(
        default=None, 
        max_length=255,
        description="Palavras-chave para busca, separadas por vírgula (Regionalismos)",
        examples=["macaxeira, aipim, castelinha, pão-de-pobre"]
    )
    
    category_id: UUID = Field(
        ..., 
        description="ID da categoria a qual este produto pertence"
    )
    
    taxonomy_code: Optional[str] = Field(
        default=None, 
        max_length=50,
        description="Código interno de taxonomia ou classificação"
    )
    
    ncm_code: Optional[str] = Field(
        default=None, 
        min_length=8, 
        max_length=8,
        pattern=r"^\d{8}$", # Garante que são apenas 8 dígitos numéricos
        description="Código NCM (Nomenclatura Comum do Mercosul) para fins fiscais",
        examples=["07141000"]
    )
    
    description_template: Optional[str] = Field(
        default=None,
        description="Sugestão de descrição para ajudar o produtor na hora do cadastro"
    )
    
    image_url: Optional[str] = Field(
        default=None,
        description="Imagem de referência do produto ('Foto Boneco')"
    )

class GlobalProductCreate(GlobalProductBase):
    """Payload para cadastrar um novo produto no catálogo mestre."""
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "Tomate Carmem",
                    "scientific_name": "Solanum lycopersicum",
                    "synonyms": "tomate longa vida, tomate salada",
                    "category_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                    "ncm_code": "07020000",
                    "image_url": "https://agrolocal.com/imgs/tomate-carmem.jpg"
                }
            ]
        }
    )

class GlobalProductRead(GlobalProductBase, TimestampSchema):
    """Retorno completo do produto global."""
    id: UUID = Field(description="ID único do produto global")
    
    status: ProductStatus = Field(
        description="Status de curadoria (PENDING, APPROVED, etc)"
    )
    
    suggested_by_id: Optional[UUID] = Field(
        default=None,
        description="ID do usuário que sugeriu este produto (se houver)"
    )