from typing import Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from app.domain.entities.transaction import Transaction
from app.domain.repositories.transaction_repository import ITransactionRepository
from app.infrastructure.models.order_model import OrderModel
from app.infrastructure.models.transaction_model import TransactionModel
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl 

class TransactionRepositoryImpl(ITransactionRepository):
    def __init__(self, db_session: Session):
        self.db = db_session
        self.order_repo = OrderRepositoryImpl(db_session) # Usado para traduzir os pedidos aninhados

    def _to_domain(self, model: TransactionModel) -> Transaction:
        # Traduzimos todos os pedidos do banco de volta para o Domínio
        domain_orders = [self.order_repo._to_domain(order_model) for order_model in model.orders]
        
        transaction = Transaction(
            payment_method=model.payment_method,
            orders=domain_orders,
            installments=model.installments,
            id=model.id,
            status=model.status,
            external_transaction_id=model.external_transaction_id,
            failure_reason=model.failure_reason,
            pix_qr_code_base64=model.pix_qr_code_base64,
            pix_copy_paste=model.pix_copy_paste,
            pix_expiration=model.pix_expiration,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
        # Forçamos o amount a ser exatamente o que está no banco
        transaction.amount = Decimal(str(model.amount)) 
        return transaction

    def save(self, transaction: Transaction) -> Transaction:
        # Salva a Transação Principal
        model = TransactionModel(
            id=transaction.id, payment_method=transaction.payment_method,
            amount=transaction.amount, installments=transaction.installments,
            status=transaction.status, external_transaction_id=transaction.external_transaction_id,
            failure_reason=transaction.failure_reason, pix_qr_code_base64=transaction.pix_qr_code_base64,
            pix_copy_paste=transaction.pix_copy_paste, pix_expiration=transaction.pix_expiration,
            created_at=transaction.created_at, updated_at=transaction.updated_at
        )
        self.db.merge(model)
        self.db.commit()

        # Vincula a Transação aos Pedidos e salva os pedidos (Cascade Manual Controlado)
        for pedido in transaction.orders:
            # Salva as alterações da entidade (como a mudança de status para PAID)
            self.order_repo.save(pedido)
            
            # Forma limpa e segura de atualizar a Foreign Key via ORM
            db_order = self.db.query(OrderModel).filter(OrderModel.id == pedido.id).first()
            if db_order:
                db_order.transaction_id = transaction.id
        
        self.db.commit()
        return transaction

    def get_by_id(self, transaction_id: UUID) -> Optional[Transaction]:
        model = self.db.query(TransactionModel).filter(TransactionModel.id == transaction_id).first()
        return self._to_domain(model) if model else None

    def get_by_external_id(self, external_id: str) -> Optional[Transaction]:
        model = self.db.query(TransactionModel).filter(TransactionModel.external_transaction_id == external_id).first()
        return self._to_domain(model) if model else None