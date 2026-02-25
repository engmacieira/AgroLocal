from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.review import Review
from app.domain.repositories.review_repository import IReviewRepository
from app.infrastructure.models.review_model import ReviewModel

class ReviewRepositoryImpl(IReviewRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def _to_domain(self, model: ReviewModel) -> Review:
        review = Review(
            order_id=model.order_id,
            customer_id=model.customer_id,
            producer_id=model.producer_id,
            rating=model.rating,
            comment=model.comment,
            photo_url=model.photo_url,
            id=model.id,
            created_at=model.created_at
        )
        return review

    def save(self, review: Review) -> Review:
        model = ReviewModel(
            id=review.id, order_id=review.order_id,
            customer_id=review.customer_id, producer_id=review.producer_id,
            rating=review.rating, comment=review.comment,
            photo_url=review.photo_url, created_at=review.created_at
        )
        self.db.merge(model)
        self.db.commit()
        return review

    def get_by_id(self, review_id: UUID) -> Optional[Review]:
        model = self.db.query(ReviewModel).filter(ReviewModel.id == review_id).first()
        return self._to_domain(model) if model else None

    def get_by_order_id(self, order_id: UUID) -> Optional[Review]:
        model = self.db.query(ReviewModel).filter(ReviewModel.order_id == order_id).first()
        return self._to_domain(model) if model else None

    def get_by_producer_id(self, producer_id: UUID, skip: int = 0, limit: int = 100) -> List[Review]:
        models = self.db.query(ReviewModel).filter(
            ReviewModel.producer_id == producer_id
        ).order_by(ReviewModel.created_at.desc()).offset(skip).limit(limit).all()
        
        return [self._to_domain(m) for m in models]