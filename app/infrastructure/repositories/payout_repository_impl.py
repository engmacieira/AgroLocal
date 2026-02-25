from typing import List, Optional
from uuid import UUID
from decimal import Decimal
from sqlalchemy.orm import Session
from app.domain.entities.payout import Payout, PayoutStatus
from app.domain.repositories.payout_repository import IPayoutRepository
from app.infrastructure.models.payout_model import PayoutModel

class PayoutRepositoryImpl(IPayoutRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def _to_domain(self, model: PayoutModel) -> Payout:
        payout = Payout(
            order_id=model.order_id,
            producer_id=model.producer_id,
            target_pix_key_snapshot=model.target_pix_key_snapshot,
            amount_gross=Decimal(str(model.amount_gross)),
            amount_fee=Decimal(str(model.amount_fee)),
            id=model.id,
            status=model.status,
            scheduled_for=model.scheduled_for,
            processed_at=model.processed_at,
            bank_transaction_id=model.bank_transaction_id,
            proof_url=model.proof_url,
            failure_reason=model.failure_reason,
            notes=model.notes,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
        return payout

    def save(self, payout: Payout) -> Payout:
        model = PayoutModel(
            id=payout.id, order_id=payout.order_id, producer_id=payout.producer_id,
            status=payout.status, amount_gross=payout.amount_gross,
            amount_fee=payout.amount_fee, amount_net=payout.amount_net,
            target_pix_key_snapshot=payout.target_pix_key_snapshot,
            scheduled_for=payout.scheduled_for, processed_at=payout.processed_at,
            bank_transaction_id=payout.bank_transaction_id, proof_url=payout.proof_url,
            failure_reason=payout.failure_reason, notes=payout.notes,
            created_at=payout.created_at, updated_at=payout.updated_at
        )
        self.db.merge(model)
        self.db.commit()
        return payout

    def get_by_id(self, payout_id: UUID) -> Optional[Payout]:
        model = self.db.query(PayoutModel).filter(PayoutModel.id == payout_id).first()
        return self._to_domain(model) if model else None

    def get_by_order_id(self, order_id: UUID) -> Optional[Payout]:
        model = self.db.query(PayoutModel).filter(PayoutModel.order_id == order_id).first()
        return self._to_domain(model) if model else None

    def get_pending_by_producer(self, producer_id: UUID) -> List[Payout]:
        models = self.db.query(PayoutModel).filter(
            PayoutModel.producer_id == producer_id,
            PayoutModel.status.in_([PayoutStatus.SCHEDULED, PayoutStatus.PROCESSING])
        ).all()
        return [self._to_domain(m) for m in models]