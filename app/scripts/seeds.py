# Arquivo: scripts/seeds.py

import sys
import os
from datetime import date, datetime, timedelta
from decimal import Decimal

# Ajuste do PATH para encontrar a pasta 'app'
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(BASE_DIR)

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user_model import User, UserRole, ProducerProfile
from app.models.address_model import Address, AddressType
from app.models.catalog_model import Category, GlobalProduct, ProductStatus
from app.models.product_model import ProducerProduct, ProductImage, AvailabilityType
from app.models.order_model import Order, OrderItem, OrderStatus, DeliveryType
from app.models.transaction_model import Transaction, TransactionStatus, PaymentMethod
from app.models.payout_model import Payout, PayoutStatus
from app.models.review_model import Review
from app.models.audit_model import AuditLog, AuditAction

def seed_db():
    db: Session = SessionLocal()
    print("🌱 Iniciando o povoamento completo do AgroLocal...")

    try:
        # --- 1. CATEGORIAS ---
        print("   - Criando categorias...")
        cat_frutas = Category(name="Frutas", slug="frutas", icon_url="🍎")
        cat_legumes = Category(name="Legumes", slug="legumes", icon_url="🥦")
        db.add_all([cat_frutas, cat_legumes])
        db.flush()

        # --- 2. USUÁRIOS (Admin, Produtor, Cliente) ---
        print("   - Criando usuários...")
        # Nota: Usando hash provisório conforme discutido na Sprint 01
        dummy_hash = "hash_provisorio"
        
        admin = User(full_name="Admin Sistema", email="admin@agro.com", password_hash=dummy_hash, role=UserRole.ADMIN, is_verified=True)
        produtor = User(full_name="João do Campo", email="joao@fazenda.com", password_hash=dummy_hash, role=UserRole.PRODUTOR, is_verified=True)
        cliente = User(full_name="Maria Silva", email="maria@cliente.com", password_hash=dummy_hash, role=UserRole.CLIENTE, is_verified=True)
        
        db.add_all([admin, produtor, cliente])
        db.flush()

        # --- 3. ENDEREÇOS ---
        print("   - Criando endereços...")
        addr_rural = Address(user_id=produtor.id, address_type=AddressType.RURAL, label="Sítio Esperança", 
                             street="Estrada da Macieira", number="Km 12", neighborhood="Zona Rural", 
                             city="São Bento", state="SP", postal_code="12345-000", reference_point="Perto da mangueira grande")
        
        addr_urbano = Address(user_id=cliente.id, address_type=AddressType.RESIDENCIAL, label="Minha Casa", 
                              street="Rua das Flores", number="123", neighborhood="Centro", 
                              city="São Bento", state="SP", postal_code="12345-100", is_default=True)
        
        db.add_all([addr_rural, addr_urbano])
        db.flush()

        # --- 4. PERFIL DO PRODUTOR ---
        print("   - Criando perfil do produtor...")
        perfil_joao = ProducerProfile(user_id=produtor.id, cpf_cnpj="123.456.789-00", pix_key="joao@pix.com", 
                                      store_name="Horta do João", bio="Produtos sem agrotóxicos.")
        db.add(perfil_joao)
        db.flush()

        # --- 5. CATÁLOGO GLOBAL ---
        print("   - Criando catálogo mestre...")
        prod_global_tomate = GlobalProduct(name="Tomate Carmem", category_id=cat_legumes.id, status=ProductStatus.APPROVED, suggested_by_id=admin.id)
        prod_global_maca = GlobalProduct(name="Maçã Gala", category_id=cat_frutas.id, status=ProductStatus.APPROVED)
        db.add_all([prod_global_tomate, prod_global_maca])
        db.flush()

        # --- 6. OFERTAS DO PRODUTOR (PRODUTOS) ---
        print("   - Criando ofertas reais...")
        oferta_tomate = ProducerProduct(producer_id=perfil_joao.id, global_product_id=prod_global_tomate.id, 
                                        price=Decimal("7.50"), unit="kg", stock_quantity=50.0, 
                                        availability_type=AvailabilityType.PRONTA_ENTREGA)
        db.add(oferta_tomate)
        db.flush()
        
        # Imagem do produto
        img_tomate = ProductImage(producer_product_id=oferta_tomate.id, url="https://link_da_foto.jpg", is_primary=True)
        db.add(img_tomate)

        # --- 7. PEDIDO E ITENS ---
        print("   - Criando pedido de teste...")
        pedido = Order(customer_id=cliente.id, producer_id=produtor.id, status=OrderStatus.PAID, 
                       total_amount=Decimal("15.00"), delivery_type=DeliveryType.DOMICILIO, 
                       delivery_address_snapshot="Rua das Flores, 123", platform_fee_value=Decimal("1.50"), 
                       producer_net_value=Decimal("13.50"))
        db.add(pedido)
        db.flush()

        item = OrderItem(order_id=pedido.id, product_id=oferta_tomate.id, product_name_snapshot="Tomate Carmem", 
                         unit_snapshot="kg", unit_price_snapshot=Decimal("7.50"), quantity=2.0, subtotal=Decimal("15.00"))
        db.add(item)

        # --- 8. FINANCEIRO (TRANSATION & PAYOUT) ---
        print("   - Criando registros financeiros...")
        transacao = Transaction(order_id=pedido.id, payment_method=PaymentMethod.PIX, amount=Decimal("15.00"), 
                                status=TransactionStatus.APPROVED, external_transaction_id="E2EID-987654321")
        
        repasse = Payout(order_id=pedido.id, producer_id=perfil_joao.id, status=PayoutStatus.SCHEDULED, 
                         amount_gross=Decimal("15.00"), amount_fee=Decimal("1.50"), amount_net=Decimal("13.50"), 
                         target_pix_key_snapshot="joao@pix.com", scheduled_for=datetime.now() + timedelta(days=1))
        
        db.add_all([transacao, repasse])

        # --- 9. AVALIAÇÃO ---
        print("   - Criando review...")
        review = Review(author_id=cliente.id, producer_id=perfil_joao.id, order_id=pedido.id, 
                        rating=5, comment="Tomates muito frescos!")
        db.add(review)

        # --- 10. AUDITORIA ---
        print("   - Criando log de auditoria...")
        audit = AuditLog(table_name="orders", record_id=1, action=AuditAction.CREATE, actor_id=cliente.id, 
                         ip_address="127.0.0.1", new_values={"status": "CREATED", "total": 15.0})
        db.add(audit)

        db.commit()
        print("\n🚀 BANCO POVOADO COM SUCESSO! Todas as tabelas têm dados de teste.")

    except Exception as e:
        print(f"\n❌ ERRO NO SEED: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()