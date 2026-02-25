import enum
import uuid
from decimal import Decimal
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime, timezone, date

class AvailabilityType(str, enum.Enum):
    """Define a logística de disponibilidade do item."""
    PRONTA_ENTREGA = "PRONTA_ENTREGA"
    ENCOMENDA = "ENCOMENDA"

class DeliveryType(str, enum.Enum):
    """Tipos de entrega que o produtor disponibiliza."""
    DOMICILIO = "DOMICILIO"
    RETIRADA_PRODUTOR = "RETIRADA_PRODUTOR"
    FEIRA_LOCAL = "FEIRA_LOCAL"

@dataclass(kw_only=True)
class DeliveryOption:
    """Opção de entrega/retirada para uma oferta específica."""
    delivery_type: DeliveryType
    fee: Decimal = Decimal("0.00")
    schedule: Optional[str] = None # Ex: "Sábados das 08h às 12h"
    is_enabled: bool = True
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __post_init__(self):
        if self.fee < Decimal("0.00"):
            raise ValueError("A taxa de entrega não pode ser negativa")

@dataclass(kw_only=True)
class ProductImage:
    """Entidade: Foto real da colheita/produto do produtor."""
    url: str
    is_primary: bool = False
    
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass(kw_only=True)
class ProducerProduct:
    """
    Entidade: A Oferta (Prateleira).
    Conecta o Produtor ao Produto Global, definindo preço, estoque e agora logística!
    """
    producer_id: uuid.UUID
    global_product_id: uuid.UUID
    price: Decimal
    
    # Detalhes Logísticos
    unit: str = "kg"
    stock_quantity: float = 0.0
    minimum_order_quantity: float = 1.0
    availability_type: AvailabilityType = AvailabilityType.PRONTA_ENTREGA
    
    # Qualidade e Frescor
    description: Optional[str] = None
    harvest_date: Optional[date] = None
    
    # Entidades Filhas (Agregados)
    images: List[ProductImage] = field(default_factory=list)
    delivery_options: List[DeliveryOption] = field(default_factory=list) # <-- NOVA LISTA
    
    # Controlo
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    is_active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = None

    def __post_init__(self):
        """Validação de regras de negócio logo ao instanciar."""
        if self.price <= Decimal("0.00"):
            raise ValueError("O preço da oferta deve ser maior que zero")
        if self.minimum_order_quantity <= 0.0:
            raise ValueError("A quantidade mínima do pedido deve ser maior que zero")

    # --- Comportamentos (Regras de Negócio) ---

    def update_stock(self, add_quantity: float) -> None:
        new_stock = self.stock_quantity + add_quantity
        if new_stock < 0.0:
            raise ValueError("O estoque não pode ficar negativo")
        self.stock_quantity = new_stock
        self.updated_at = datetime.now(timezone.utc)

    def update_details(self, new_price: Optional[Decimal] = None, new_description: Optional[str] = None) -> None:
        if new_price is not None:
            if new_price <= Decimal("0.00"):
                raise ValueError("O preço da oferta deve ser maior que zero")
            self.price = new_price
        if new_description is not None:
            self.description = new_description
        self.updated_at = datetime.now(timezone.utc)

    def add_image(self, url: str, is_primary: bool = False) -> None:
        nova_imagem = ProductImage(url=url, is_primary=is_primary)
        self.images.append(nova_imagem)
        self.updated_at = datetime.now(timezone.utc)

    def set_delivery_options(self, options: List[DeliveryOption]) -> None:
        """Atualiza a grade de logística do produto."""
        self.delivery_options = options
        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)