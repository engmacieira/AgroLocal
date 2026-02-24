from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.address import Address
from app.domain.repositories.address_repository import IAddressRepository
from app.infrastructure.models.address_model import AddressModel

class AddressRepositoryImpl(IAddressRepository):
    """Implementação concreta do Repositório de Endereços via SQLAlchemy."""
    
    def __init__(self, db_session: Session):
        self.db = db_session

    def _to_domain(self, model: AddressModel) -> Address:
        return Address(
            id=model.id,
            user_id=model.user_id,
            address_type=model.address_type,
            label=model.label,
            street=model.street,
            number=model.number,
            complement=model.complement,
            neighborhood=model.neighborhood,
            city=model.city,
            state=model.state,
            postal_code=model.postal_code,
            reference_point=model.reference_point,
            latitude=model.latitude,
            longitude=model.longitude,
            is_default=model.is_default,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: Address) -> AddressModel:
        return AddressModel(
            id=entity.id,
            user_id=entity.user_id,
            address_type=entity.address_type,
            label=entity.label,
            street=entity.street,
            number=entity.number,
            complement=entity.complement,
            neighborhood=entity.neighborhood,
            city=entity.city,
            state=entity.state,
            postal_code=entity.postal_code,
            reference_point=entity.reference_point,
            latitude=entity.latitude,
            longitude=entity.longitude,
            is_default=entity.is_default,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def save(self, address: Address) -> Address:
        model = self._to_model(address)
        self.db.merge(model)
        self.db.commit()
        return address

    def get_by_id(self, address_id: UUID) -> Optional[Address]:
        model = self.db.query(AddressModel).filter(AddressModel.id == address_id).first()
        return self._to_domain(model) if model else None

    def get_by_user_id(self, user_id: UUID, skip: int = 0, limit: int = 100) -> List[Address]:
        models = (
            self.db.query(AddressModel)
            .filter(AddressModel.user_id == user_id, AddressModel.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_domain(m) for m in models]

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Address]:
        models = (
            self.db.query(AddressModel)
            .filter(AddressModel.is_active == True)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return [self._to_domain(m) for m in models]
    
    def delete(self, address_id: UUID) -> None:
        address = self.get_by_id(address_id)
        if address:
            address.deactivate()
            self.save(address)