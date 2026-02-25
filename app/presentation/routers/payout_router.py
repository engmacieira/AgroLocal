from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.infrastructure.repositories.payout_repository_impl import PayoutRepositoryImpl
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl

from app.application.use_cases.payout_management import (
    SchedulePayoutUseCase, ProcessPayoutUseCase, FailPayoutUseCase
)
from app.presentation.schemas.payout_schema import (
    SchedulePayoutRequest, ProcessPayoutRequest, FailPayoutRequest, PayoutResponse
)

router = APIRouter(prefix="/payouts", tags=["Payouts (Repasses)"])

@router.post("/schedule", response_model=PayoutResponse, status_code=status.HTTP_201_CREATED)
def schedule_payout(request: SchedulePayoutRequest, db: Session = Depends(get_db)):
    """Agenda um repasse para o produtor calculando a taxa da plataforma."""
    payout_repo = PayoutRepositoryImpl(db)
    order_repo = OrderRepositoryImpl(db)
    use_case = SchedulePayoutUseCase(payout_repo, order_repo)
    
    try:
        return use_case.execute(request.order_id, request.target_pix_key, request.fee_percentage)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{payout_id}/process", response_model=PayoutResponse)
def process_payout(payout_id: UUID, request: ProcessPayoutRequest, db: Session = Depends(get_db)):
    """Admin confirma a transferência, anexa o comprovante e finaliza a Ordem."""
    payout_repo = PayoutRepositoryImpl(db)
    order_repo = OrderRepositoryImpl(db)
    use_case = ProcessPayoutUseCase(payout_repo, order_repo)
    
    try:
        return use_case.execute(payout_id, request.bank_transaction_id, request.proof_url)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/{payout_id}/fail", response_model=PayoutResponse)
def fail_payout(payout_id: UUID, request: FailPayoutRequest, db: Session = Depends(get_db)):
    """Admin reporta falha bancária ao tentar pagar o produtor."""
    payout_repo = PayoutRepositoryImpl(db)
    use_case = FailPayoutUseCase(payout_repo)
    
    try:
        return use_case.execute(payout_id, request.reason)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/producer/{producer_id}/pending", response_model=List[PayoutResponse])
def get_pending_payouts(producer_id: UUID, db: Session = Depends(get_db)):
    """Lista os repasses que o produtor tem a receber."""
    repo = PayoutRepositoryImpl(db)
    return repo.get_pending_by_producer(producer_id)