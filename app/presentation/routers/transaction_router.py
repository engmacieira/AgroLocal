from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.core.database import get_db
from app.infrastructure.repositories.transaction_repository_impl import TransactionRepositoryImpl
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl

from app.application.use_cases.transaction_management import GeneratePaymentUseCase, ProcessWebhookUseCase
from app.presentation.schemas.transaction_schema import GeneratePaymentRequest, WebhookPayloadRequest, TransactionResponse

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def generate_payment(request: GeneratePaymentRequest, db: Session = Depends(get_db)):
    """Gera o pagamento (PIX) unificado para os pedidos do carrinho."""
    trans_repo = TransactionRepositoryImpl(db)
    order_repo = OrderRepositoryImpl(db)
    use_case = GeneratePaymentUseCase(trans_repo, order_repo)
    
    try:
        return use_case.execute(request.order_ids, request.payment_method)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.post("/{transaction_id}/webhook", response_model=TransactionResponse)
def process_webhook(transaction_id: UUID, payload: WebhookPayloadRequest, db: Session = Depends(get_db)):
    """Simula o recebimento do Webhook do Gateway (Aprovação ou Falha)."""
    repo = TransactionRepositoryImpl(db)
    use_case = ProcessWebhookUseCase(repo)
    
    try:
        return use_case.execute(
            transaction_id=transaction_id, 
            external_id=payload.external_transaction_id,
            is_approved=payload.is_approved,
            failure_reason=payload.failure_reason
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))