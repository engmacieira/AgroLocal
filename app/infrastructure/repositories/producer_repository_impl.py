from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.producer_profile import ProducerProfile
from app.domain.repositories.producer_repository import IProducerRepository
from app.infrastructure.models.producer_model import ProducerModel

class ProducerRepositoryImpl(IProducerRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def _to_domain(self, model: ProducerModel) -> ProducerProfile:
        return ProducerProfile(
            id=model.id,
            user_id=model.user_id,
            store_name=model.store_name,
            document=model.document,
            pix_key=model.pix_key,
            bio=model.bio,
            cover_image=model.cover_image,
            rating=model.rating,
            review_count=model.review_count,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: ProducerProfile) -> ProducerModel:
        return ProducerModel(
            id=entity.id,
            user_id=entity.user_id,
            store_name=entity.store_name,
            document=entity.document,
            pix_key=entity.pix_key,
            bio=entity.bio,
            cover_image=entity.cover_image,
            rating=entity.rating,
            review_count=entity.review_count,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def save(self, profile: ProducerProfile) -> ProducerProfile:
        model = self._to_model(profile)
        self.db.merge(model)
        self.db.commit()
        return profile

    def get_by_id(self, profile_id: UUID) -> Optional[ProducerProfile]:
        model = self.db.query(ProducerModel).filter(ProducerModel.id == profile_id).first()
        return self._to_domain(model) if model else None

    def get_by_user_id(self, user_id: UUID) -> Optional[ProducerProfile]:
        model = self.db.query(ProducerModel).filter(
            ProducerModel.user_id == user_id, 
            ProducerModel.is_active == True
        ).first()
        return self._to_domain(model) if model else None

    def get_by_document(self, document: str) -> Optional[ProducerProfile]:
        model = self.db.query(ProducerModel).filter(ProducerModel.document == document).first()
        return self._to_domain(model) if model else None

    def get_all_active(self, skip: int = 0, limit: int = 100) -> List[ProducerProfile]:
        models = self.db.query(ProducerModel).filter(ProducerModel.is_active == True).offset(skip).limit(limit).all()
        return [self._to_domain(m) for m in models]

    def delete(self, profile_id: UUID) -> None:
        profile = self.get_by_id(profile_id)
        if profile:
            profile.deactivate()
            self.save(profile)