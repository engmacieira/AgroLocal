from pydantic import Field, ConfigDict
from typing import Optional
from uuid import UUID
from app.models.address_model import AddressType
from app.schemas.base_schema import BaseSchema, TimestampSchema

class AddressBase(BaseSchema):
    """
    Schema base contendo os campos comuns de endereço.
    Utiliza validações de tamanho para garantir compatibilidade com o banco de dados.
    """
    address_type: AddressType = Field(
        default=AddressType.RESIDENCIAL,
        description="Classificação do local (Residencial, Comercial, Rural, etc)"
    )
    
    label: Optional[str] = Field(
        default=None, 
        max_length=50,
        description="Nome amigável para identificar o endereço",
        examples=["Minha Casa", "Sítio Santa Rita", "Ponto de Encontro da Praça"]
    )
    
    street: str = Field(
        ..., 
        max_length=150,
        description="Logradouro (Rua, Avenida, Estrada)"
    )
    
    number: str = Field(
        ..., 
        max_length=20,
        description="Número, 'S/N' ou Km (para áreas rurais)"
    )
    
    complement: Optional[str] = Field(
        default=None, 
        max_length=100,
        description="Apartamento, Bloco, Fundos, etc"
    )
    
    neighborhood: str = Field(
        ..., 
        max_length=100,
        description="Bairro ou Localidade"
    )
    
    city: str = Field(
        ..., 
        max_length=100,
        description="Cidade / Município"
    )
    
    state: str = Field(
        ..., 
        min_length=2, 
        max_length=2,
        pattern=r"^[A-Z]{2}$",
        description="Sigla do Estado (UF) em maiúsculas (Ex: SP, MG)"
    )
    
    postal_code: str = Field(
        ..., 
        min_length=8, 
        max_length=9,
        description="CEP (apenas números ou com hífen)",
        examples=["12345-000", "12345678"]
    )
    
    reference_point: Optional[str] = Field(
        default=None, 
        max_length=255,
        description="Referência visual para facilitar a entrega (Crucial para áreas rurais)"
    )
    
    # Validação Geográfica
    latitude: Optional[float] = Field(
        default=None, 
        ge=-90, 
        le=90,
        description="Coordenada Latitude (entre -90 e 90)"
    )
    
    longitude: Optional[float] = Field(
        default=None, 
        ge=-180, 
        le=180,
        description="Coordenada Longitude (entre -180 e 180)"
    )

class AddressCreate(AddressBase):
    """
    Payload para criação de um novo endereço.
    """
    # Configuração para exibir um exemplo rico no Swagger UI
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "address_type": "RURAL",
                    "label": "Sítio Principal",
                    "street": "Estrada do Barreiro",
                    "number": "Km 12",
                    "neighborhood": "Zona Rural",
                    "city": "São Bento do Sapucaí",
                    "state": "SP",
                    "postal_code": "12490-000",
                    "reference_point": "Entrada à direita após a igreja azul",
                    "latitude": -22.689,
                    "longitude": -45.739
                }
            ]
        }
    )

class AddressRead(AddressBase, TimestampSchema):
    """
    Schema de resposta da API contendo IDs e Timestamps.
    """
    id: UUID = Field(description="Identificador único do endereço")
    user_id: UUID = Field(description="ID do usuário dono deste endereço")