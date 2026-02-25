import uuid
from typing import List
from app.domain.entities.transaction import Transaction, PaymentMethod
from app.domain.repositories.transaction_repository import ITransactionRepository
from app.domain.repositories.order_repository import IOrderRepository

class GeneratePaymentUseCase:
    """Caso de Uso: Gera um pagamento unificado (Ex: PIX) para múltiplos pedidos."""
    def __init__(self, transaction_repository: ITransactionRepository, order_repository: IOrderRepository):
        self.transaction_repository = transaction_repository
        self.order_repository = order_repository

    def execute(self, order_ids: List[uuid.UUID], payment_method: PaymentMethod = PaymentMethod.PIX) -> Transaction:
        if not order_ids:
            raise ValueError("Nenhum pedido informado para pagamento")

        pedidos = []
        for o_id in order_ids:
            pedido = self.order_repository.get_by_id(o_id)
            if not pedido:
                raise ValueError(f"Pedido {o_id} não encontrado")
            if pedido.status != "CREATED":
                raise ValueError(f"O pedido {o_id} já não está pendente de pagamento")
            pedidos.append(pedido)

        # Cria a Transação Unificada
        transacao = Transaction(payment_method=payment_method, orders=pedidos)
        
        # Aqui, numa app real, chamaríamos a API do MercadoPago/Stripe para gerar o QR Code.
        # Vamos simular a geração para o nosso MVP:
        if payment_method == PaymentMethod.PIX:
            transacao.pix_copy_paste = f"00020101021126580014br.gov.bcb.pix0136{uuid.uuid4()}"
            
        return self.transaction_repository.save(transacao)

class ProcessWebhookUseCase:
    """Caso de Uso: Recebe o aviso do Gateway de que o cliente pagou."""
    def __init__(self, transaction_repository: ITransactionRepository):
        self.transaction_repository = transaction_repository

    def execute(self, transaction_id: uuid.UUID, external_id: str, is_approved: bool, failure_reason: str = None) -> Transaction:
        transacao = self.transaction_repository.get_by_id(transaction_id)
        if not transacao:
            raise ValueError("Transação não encontrada")

        if is_approved:
            transacao.approve(external_id=external_id)
        else:
            transacao.fail(reason=failure_reason or "Pagamento recusado pelo banco")

        return self.transaction_repository.save(transacao)