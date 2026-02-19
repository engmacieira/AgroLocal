from pydantic import Field, ConfigDict
from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from app.models.order_model import OrderStatus, DeliveryType
from app.schemas.base_schema import BaseSchema, TimestampSchema

# --- Itens do Pedido (Linhas da Nota) ---

class OrderItemBase(BaseSchema):
    """
    Schema base para adicionar itens ao carrinho.
    """
    product_id: UUID = Field(
        ..., 
        description="ID do produto ofertado pelo produtor (ProducerProduct)"
    )
    
    quantity: float = Field(
        ..., 
        gt=0,
        description="Quantidade desejada (respeitando a unidade do produto, ex: Kg, Maço)",
        examples=[1.5, 5.0]
    )

class OrderItemRead(BaseSchema):
    """
    Representação do item comprado.
    Nota: Todos os dados aqui são SNAPSHOTS (cópias imutáveis) do momento da compra.
    Mesmo que o produtor mude o preço depois, este registro permanece intacto.
    """
    id: UUID = Field(description="ID único do item do pedido")
    
    product_name_snapshot: str = Field(
        description="Nome do produto no momento da compra (Ex: Tomate Carmem)"
    )
    
    unit_snapshot: str = Field(
        description="Unidade de medida no momento da compra (Ex: kg, dz)"
    )
    
    unit_price_snapshot: Decimal = Field(
        description="Preço unitário pago"
    )
    
    quantity: float = Field(description="Quantidade comprada")
    
    subtotal: Decimal = Field(
        description="Valor total da linha (Preço x Quantidade)"
    )

# --- Pedido (Cabeçalho) ---

class OrderCreate(BaseSchema):
    """
    Payload para fechar um novo pedido.
    """
    producer_id: UUID = Field(
        ..., 
        description="ID do produtor que receberá o pedido"
    )
    
    items: List[OrderItemBase] = Field(
        ..., 
        min_length=1,
        description="Lista de produtos (não pode estar vazia)"
    )
    
    delivery_type: DeliveryType = Field(
        ..., 
        description="Modalidade de entrega escolhida"
    )
    
    delivery_address_snapshot: str = Field(
        ..., 
        min_length=10,
        description="Endereço completo formatado como texto para histórico (Rua, Nº, Bairro, Cidade)",
        examples=["Rua das Flores, 123 - Centro, São Bento do Sapucaí - SP"]
    )

    # Exemplo para Documentação Automática
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "producer_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                    "delivery_type": "DOMICILIO",
                    "delivery_address_snapshot": "Sítio Recanto Feliz, km 5 - Zona Rural",
                    "items": [
                        {
                            "product_id": "b2f4c810-1d2a-4f5b-9c8e-2a3b4c5d6e7f",
                            "quantity": 2.5
                        },
                        {
                            "product_id": "c3d5e712-3a4b-5c6d-7e8f-9a0b1c2d3e4f",
                            "quantity": 1.0
                        }
                    ]
                }
            ]
        }
    )

class OrderRead(TimestampSchema):
    """
    Resumo do Pedido para listagens e detalhes.
    """
    id: UUID = Field(description="ID único do pedido")
    
    customer_id: UUID = Field(description="ID do cliente que comprou")
    producer_id: UUID = Field(description="ID do produtor vendedor")
    
    status: OrderStatus = Field(
        description="Estado atual do fluxo (CREATED, PAID, DELIVERED, etc)"
    )
    
    total_amount: Decimal = Field(
        description="Valor total a pagar (Produtos + Frete)"
    )
    
    delivery_type: DeliveryType = Field(description="Tipo de entrega")
    
    delivery_fee: Decimal = Field(
        description="Valor do frete cobrado (0.00 se for retirada)"
    )
    
    items: List[OrderItemRead] = Field(
        description="Lista detalhada dos itens comprados"
    )