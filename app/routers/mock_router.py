from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from uuid import uuid4, UUID
from decimal import Decimal
from datetime import datetime, timedelta

# --- 1. Imports dos Models (Enums e Tipos) ---
# Extraídos de: app/models/
from app.models.user_model import UserRole
from app.models.catalog_model import ProductStatus
from app.models.product_model import AvailabilityType
from app.models.order_model import OrderStatus, DeliveryType
from app.models.address_model import AddressType
from app.models.transaction_model import TransactionStatus, PaymentMethod
from app.models.payout_model import PayoutStatus
from app.models.audit_model import AuditAction

# --- 2. Imports de TODOS os Schemas ---
# Extraídos de: app/schemas/
from app.schemas.user_schema import UserRead, ProducerProfileRead, UserCreate, UserBase
from app.schemas.address_schema import AddressRead
from app.schemas.catalog_schema import CategoryRead, GlobalProductRead
from app.schemas.product_schema import ProducerProductRead, ProductImageRead
from app.schemas.order_schema import OrderRead, OrderItemRead, OrderCreate
from app.schemas.review_schema import ReviewRead
from app.schemas.transaction_schema import TransactionRead, TransactionCreate
from app.schemas.payout_schema import PayoutRead
from app.schemas.audit_schema import AuditLogRead

router = APIRouter(prefix="/mocks", tags=["Mocks (Frontend Dev)"])

# ==============================================================================
# 🔐 AUTH & USER (Para tela de Login e Perfil)
# ==============================================================================

@router.post("/auth/login")
def mock_login():
    """Simula um login retornando um Token JWT falso."""
    return {
        "access_token": "ey12345fake.token.jwt",
        "token_type": "bearer",
        "user_role": "PRODUTOR"
    }

@router.get("/users/me", response_model=UserRead)
def get_mock_my_profile():
    """Retorna o perfil do usuário logado (Simulando um Produtor)."""
    return UserRead(
        id=uuid4(),
        email="joao@fazenda.com",
        full_name="João Agricultor",
        phone="(12) 99999-1234",
        role=UserRole.PRODUTOR,
        is_active=True,
        is_verified=True,
        avatar_url="https://i.pravatar.cc/300?img=11",
        created_at=datetime.now(),
        updated_at=datetime.now(),
        producer_profile=ProducerProfileRead(
            id=uuid4(),
            cpf_cnpj="12345678901",
            pix_key="joao@pix.com",
            store_name="Sítio Recanto Verde",
            bio="Cultivo orgânico familiar desde 1995. Entregamos saúde na sua mesa.",
            rating=4.8,
            review_count=120
        )
    )

@router.get("/users/me/addresses", response_model=List[AddressRead])
def get_mock_addresses():
    """Retorna endereços para a tela de 'Selecionar Endereço de Entrega'."""
    return [
        AddressRead(
            id=uuid4(),
            user_id=uuid4(),
            address_type=AddressType.RURAL,
            label="Sede do Sítio",
            street="Estrada Municipal do Barreiro",
            number="Km 5",
            neighborhood="Zona Rural",
            city="São Bento do Sapucaí",
            state="SP",
            postal_code="12490-000",
            reference_point="Porteira azul ao lado da igreja",
            latitude=-22.68,
            longitude=-45.73,
            created_at=datetime.now()
        )
    ]

# ==============================================================================
# 🍎 CATÁLOGO & VITRINE (Para Home e Busca)
# ==============================================================================

@router.get("/categories", response_model=List[CategoryRead])
def get_mock_categories():
    """Carrossel de Categorias."""
    return [
        CategoryRead(id=uuid4(), name="Frutas", slug="frutas", icon_url="🍎", is_active=True),
        CategoryRead(id=uuid4(), name="Legumes", slug="legumes", icon_url="🥦", is_active=True),
        CategoryRead(id=uuid4(), name="Laticínios", slug="laticinios", icon_url="🧀", is_active=True),
    ]

@router.get("/products/offers", response_model=List[ProducerProductRead])
def get_mock_offers():
    """Vitrine Principal: Ofertas dos produtores."""
    
    # 1. Geramos os IDs dos produtos globais antes para manter consistência
    id_tomate_global = uuid4()
    id_queijo_global = uuid4()

    return [
        ProducerProductRead(
            id=uuid4(),
            producer_id=uuid4(),
            global_product_id=id_tomate_global, # <--- O CAMPO QUE FALTAVA!
            price=Decimal("8.50"),
            unit="kg",
            stock_quantity=50.0,
            availability_type=AvailabilityType.PRONTA_ENTREGA,
            minimum_order_quantity=1.0,
            description="Tomates Carmem selecionados, muito vermelhos e doces.",
            is_active=True,
            created_at=datetime.now(),
            global_info=GlobalProductRead(
                id=id_tomate_global, # Usamos o mesmo ID aqui
                name="Tomate Carmem",
                category_id=uuid4(),
                status=ProductStatus.APPROVED,
                image_url="https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400"
            ),
            images=[
                ProductImageRead(url="https://images.unsplash.com/photo-1592924357228-91a4daadcfea?w=400", is_primary=True, id=uuid4())
            ]
        ),
        ProducerProductRead(
            id=uuid4(),
            producer_id=uuid4(),
            global_product_id=id_queijo_global, # <--- O CAMPO QUE FALTAVA!
            price=Decimal("35.00"),
            unit="unidade",
            stock_quantity=10.0,
            availability_type=AvailabilityType.ENCOMENDA,
            minimum_order_quantity=1.0,
            description="Queijo Minas Artesanal curado por 30 dias.",
            is_active=True,
            created_at=datetime.now(),
            global_info=GlobalProductRead(
                id=id_queijo_global, # Usamos o mesmo ID aqui
                name="Queijo Minas Curado",
                category_id=uuid4(),
                status=ProductStatus.APPROVED,
                image_url="https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=400"
            ),
            images=[
                ProductImageRead(url="https://images.unsplash.com/photo-1486297678162-eb2a19b0a32d?w=400", is_primary=True, id=uuid4())
            ]
        )
    ]

# ==============================================================================
# 📦 PEDIDOS (Para tela de Carrinho e Histórico)
# ==============================================================================

@router.post("/orders", status_code=201)
def mock_create_order(order: OrderCreate):
    """Simula a finalização do carrinho."""
    return {"message": "Pedido criado com sucesso!", "order_id": uuid4()}

@router.get("/orders", response_model=List[OrderRead])
def get_mock_orders():
    """Histórico de Pedidos (Aba 'Meus Pedidos')."""
    return [
        OrderRead(
            id=uuid4(),
            customer_id=uuid4(),
            producer_id=uuid4(),
            status=OrderStatus.DELIVERED,
            total_amount=Decimal("52.00"),
            delivery_type=DeliveryType.RETIRADA,
            delivery_fee=Decimal("0.00"),
            created_at=datetime.now() - timedelta(days=5),
            items=[
                OrderItemRead(
                    id=uuid4(),
                    product_name_snapshot="Tomate Carmem",
                    unit_snapshot="kg",
                    unit_price_snapshot=Decimal("8.50"),
                    quantity=2.0,
                    subtotal=Decimal("17.00")
                ),
                OrderItemRead(
                    id=uuid4(),
                    product_name_snapshot="Queijo Minas Curado",
                    unit_snapshot="unidade",
                    unit_price_snapshot=Decimal("35.00"),
                    quantity=1.0,
                    subtotal=Decimal("35.00")
                )
            ]
        )
    ]

# ==============================================================================
# 💳 FINANCEIRO (Checkout e Saldo do Produtor)
# ==============================================================================

@router.post("/transactions", response_model=TransactionRead)
def mock_create_transaction(tx: TransactionCreate):
    """
    Simula o Checkout: Retorna o QR Code do PIX para o usuário pagar.
    Essencial para a tela de Pagamento.
    """
    return TransactionRead(
        id=uuid4(),
        order_id=tx.order_id,
        payment_method=tx.payment_method,
        amount=tx.amount,
        installments=tx.installments,
        status=TransactionStatus.PENDING,
        # Dados Fakes do PIX para o Frontend exibir o QR Code
        pix_qr_code_base64="iVBORw0KGgoAAAANSUhEUgAA...", # Base64 fake
        pix_copy_paste="00020126580014br.gov.bcb.pix0136123e4567-e89b-12d3-a456-426614174000",
        pix_expiration=datetime.now() + timedelta(minutes=15),
        created_at=datetime.now()
    )

@router.get("/payouts", response_model=List[PayoutRead])
def get_mock_payouts():
    """
    Painel Financeiro do Produtor.
    Mostra o dinheiro que ele tem a receber (Saldo).
    """
    return [
        PayoutRead(
            id=uuid4(),
            order_id=uuid4(),
            producer_id=uuid4(),
            status=PayoutStatus.SCHEDULED,
            amount_gross=Decimal("100.00"),
            amount_fee=Decimal("10.00"),  # Taxa da plataforma
            amount_net=Decimal("90.00"),  # O que o produtor recebe
            target_pix_key_snapshot="joao@pix.com",
            scheduled_for=datetime.now() + timedelta(days=2),
            created_at=datetime.now()
        ),
        PayoutRead(
            id=uuid4(),
            order_id=uuid4(),
            producer_id=uuid4(),
            status=PayoutStatus.PAID,
            amount_gross=Decimal("50.00"),
            amount_fee=Decimal("5.00"),
            amount_net=Decimal("45.00"),
            target_pix_key_snapshot="joao@pix.com",
            processed_at=datetime.now() - timedelta(days=10),
            bank_transaction_id="E98765432120260218",
            proof_url="https://banco.com/comprovante.pdf",
            created_at=datetime.now() - timedelta(days=12)
        )
    ]

# ==============================================================================
# ⭐ REVIEWS & AUDITORIA
# ==============================================================================

@router.get("/reviews", response_model=List[ReviewRead])
def get_mock_reviews():
    """Lista de avaliações para o produtor ver sua reputação."""
    return [
        ReviewRead(
            id=uuid4(),
            order_id=uuid4(),
            producer_id=uuid4(),
            author_id=uuid4(),
            rating=5,
            comment="Produtos excelentes! Entrega rápida.",
            created_at=datetime.now() - timedelta(days=2)
        )
    ]

@router.get("/audit/logs", response_model=List[AuditLogRead])
def get_mock_audit_logs():
    """
    (Apenas Admin) Histórico de alterações.
    """
    return [
        AuditLogRead(
            id=uuid4(),
            table_name="products",
            record_id=uuid4(), # Simulando UUID
            action=AuditAction.UPDATE,
            actor_id=uuid4(),
            ip_address="192.168.1.10",
            old_values={"price": 10.00},
            new_values={"price": 12.00},
            created_at=datetime.now()
        )
    ]