from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.infrastructure.repositories.review_repository_impl import ReviewRepositoryImpl
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl

from app.application.use_cases.review_management import CreateReviewUseCase
from app.presentation.schemas.review_schema import CreateReviewRequest, ReviewResponse

router = APIRouter(prefix="/reviews", tags=["Reviews (Avaliações)"])

@router.post("/", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
def create_review(request: CreateReviewRequest, db: Session = Depends(get_db)):
    """O cliente avalia um pedido que já foi entregue."""
    review_repo = ReviewRepositoryImpl(db)
    order_repo = OrderRepositoryImpl(db)
    use_case = CreateReviewUseCase(review_repo, order_repo)
    
    try:
        return use_case.execute(
            order_id=request.order_id,
            customer_id=request.customer_id,
            rating=request.rating,
            comment=request.comment,
            photo_url=request.photo_url
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/producer/{producer_id}", response_model=List[ReviewResponse])
def get_producer_reviews(producer_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Vitrine de Reputação: Lista as avaliações que o produtor recebeu."""
    repo = ReviewRepositoryImpl(db)
    return repo.get_by_producer_id(producer_id, skip, limit)