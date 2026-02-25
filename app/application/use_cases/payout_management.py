import uuid
from decimal import Decimal
from app.domain.entities.payout import Payout
from app.domain.repositories.payout_repository import IPayoutRepository
from app.domain.repositories.order_repository import IOrderRepository

class SchedulePayoutUseCase:
    """Caso de Uso: Calcula a comissão e agenda o pagamento ao produtor."""
    def __init__(self, payout_repository: IPayoutRepository, order_repository: IOrderRepository):
        self.payout_repository = payout_repository
        self.order_repository = order_repository

    def execute(self, order_id: uuid.UUID, target_pix_key: str, fee_percentage: Decimal = Decimal("10.00")) -> Payout:
        pedido = self.order_repository.get_by_id(order_id)
        if not pedido:
            raise ValueError("Pedido não encontrado")
        
        if pedido.status != "DELIVERED":
            raise ValueError("Apenas pedidos entregues podem gerar repasse")

        # Verifica se já não existe um repasse para evitar pagamentos duplicados
        existing_payout = self.payout_repository.get_by_order_id(order_id)
        if existing_payout:
            raise ValueError("Já existe um repasse agendado para este pedido")

        # Calcula a taxa da plataforma (Ex: 10% de R$ 100,00 = R$ 10.00)
        fee_amount = (pedido.total_amount * fee_percentage) / Decimal("100.00")
        fee_amount = round(fee_amount, 2) # Garante 2 casas decimais

        repasse = Payout(
            order_id=pedido.id,
            producer_id=pedido.producer_id,
            target_pix_key_snapshot=target_pix_key,
            amount_gross=pedido.total_amount,
            amount_fee=fee_amount
        )

        return self.payout_repository.save(repasse)

class ProcessPayoutUseCase:
    """Caso de Uso: Admin confirma a transferência, anexa o comprovativo e conclui o pedido."""
    def __init__(self, payout_repository: IPayoutRepository, order_repository: IOrderRepository):
        self.payout_repository = payout_repository
        self.order_repository = order_repository

    def execute(self, payout_id: uuid.UUID, bank_transaction_id: str, proof_url: str) -> Payout:
        repasse = self.payout_repository.get_by_id(payout_id)
        if not repasse:
            raise ValueError("Repasse não encontrado")

        pedido = self.order_repository.get_by_id(repasse.order_id)
        if not pedido:
            raise ValueError("Pedido associado não encontrado")

        # 1. Atualiza e salva o Repasse como PAGO
        repasse.mark_as_paid(bank_transaction_id=bank_transaction_id, proof_url=proof_url)
        self.payout_repository.save(repasse)

        # 2. Atualiza e salva o Pedido como CONCLUÍDO (Cascade Lógico)
        pedido.mark_as_completed()
        self.order_repository.save(pedido)

        return repasse

class FailPayoutUseCase:
    """Caso de Uso: Admin reporta falha no banco (Ex: Chave PIX errada)."""
    def __init__(self, payout_repository: IPayoutRepository):
        self.payout_repository = payout_repository

    def execute(self, payout_id: uuid.UUID, reason: str) -> Payout:
        repasse = self.payout_repository.get_by_id(payout_id)
        if not repasse:
            raise ValueError("Repasse não encontrado")

        repasse.mark_as_failed(reason=reason)
        return self.payout_repository.save(repasse)