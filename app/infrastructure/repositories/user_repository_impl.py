from typing import Optional
from uuid import UUID
from sqlalchemy.orm import Session
from app.domain.entities.user import User
from app.domain.repositories.user_repository import IUserRepository
from app.infrastructure.models.user_model import UserModel

class UserRepositoryImpl(IUserRepository):
    """
    Implementação concreta do Repositório de Usuários usando SQLAlchemy.
    """
    def __init__(self, db_session: Session):
        self.db = db_session

    def _to_domain(self, model: UserModel) -> User:
        """Traduz do formato de Banco de Dados para a Entidade de Domínio."""
        return User(
            id=model.id,
            email=model.email,
            password_hash=model.password_hash,
            full_name=model.full_name,
            role=model.role,
            phone=model.phone,
            avatar_url=model.avatar_url,
            is_active=model.is_active,
            is_verified=model.is_verified,
            terms_accepted_at=model.terms_accepted_at,
            last_login=model.last_login,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: User) -> UserModel:
        """Traduz da Entidade de Domínio para o formato de Banco de Dados."""
        return UserModel(
            id=entity.id,
            email=entity.email,
            password_hash=entity.password_hash,
            full_name=entity.full_name,
            role=entity.role,
            phone=entity.phone,
            avatar_url=entity.avatar_url,
            is_active=entity.is_active,
            is_verified=entity.is_verified,
            terms_accepted_at=entity.terms_accepted_at,
            last_login=entity.last_login,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )

    def save(self, user: User) -> User:
        user_model = self._to_model(user)
        # O merge faz um "upsert": se o ID já existe, atualiza. Se não, insere.
        self.db.merge(user_model)
        self.db.commit()
        return user

    def get_by_id(self, user_id: UUID) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.id == user_id).first()
        if model:
            return self._to_domain(model)
        return None

    def get_all(self, skip: int = 0, limit: int = 100) -> list[User]:
        models = self.db.query(UserModel).offset(skip).limit(limit).all()
        return [self._to_domain(model) for model in models]
    
    def get_by_email(self, email: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.email == email).first()
        if model:
            return self._to_domain(model)
        return None

    def get_by_phone(self, phone: str) -> Optional[User]:
        model = self.db.query(UserModel).filter(UserModel.email == phone).first()
        if model:
            return self._to_domain(model)
        return None
    
    def delete(self, user_id: UUID) -> None:
        """
        No nosso caso, fazemos Soft Delete recuperando a entidade, 
        aplicando a regra de negócio e salvando.
        """
        user = self.get_by_id(user_id)
        if user:
            user.deactivate() # Regra de negócio pura!
            self.save(user)