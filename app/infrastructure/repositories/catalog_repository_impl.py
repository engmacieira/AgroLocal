from typing import List, Optional
from uuid import UUID
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.domain.entities.catalog import Category, GlobalProduct, ProductStatus
from app.domain.repositories.catalog_repository import ICategoryRepository, IGlobalProductRepository
from app.infrastructure.models.catalog_model import CategoryModel, GlobalProductModel

class CategoryRepositoryImpl(ICategoryRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def save(self, category: Category) -> Category:
        model = CategoryModel(
            id=category.id, name=category.name, slug=category.slug,
            icon_url=category.icon_url, is_active=category.is_active
        )
        self.db.merge(model)
        self.db.commit()
        return category

    def get_by_id(self, category_id: UUID) -> Optional[Category]:
        model = self.db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
        if not model: return None
        return Category(id=model.id, name=model.name, slug=model.slug, icon_url=model.icon_url, is_active=model.is_active)

    def get_by_slug(self, slug: str) -> Optional[Category]:
        model = self.db.query(CategoryModel).filter(CategoryModel.slug == slug).first()
        if not model: return None
        return Category(id=model.id, name=model.name, slug=model.slug, icon_url=model.icon_url, is_active=model.is_active)

    def get_all_active(self) -> List[Category]:
        models = self.db.query(CategoryModel).filter(CategoryModel.is_active == True).all()
        return [Category(id=m.id, name=m.name, slug=m.slug, icon_url=m.icon_url, is_active=m.is_active) for m in models]

class GlobalProductRepositoryImpl(IGlobalProductRepository):
    def __init__(self, db_session: Session):
        self.db = db_session

    def _to_domain(self, model: GlobalProductModel) -> GlobalProduct:
        return GlobalProduct(
            id=model.id, name=model.name, category_id=model.category_id,
            scientific_name=model.scientific_name, synonyms=model.synonyms,
            taxonomy_code=model.taxonomy_code, ncm_code=model.ncm_code,
            description_template=model.description_template, image_url=model.image_url,
            status=model.status, suggested_by_id=model.suggested_by_id,
            reviewed_by_id=model.reviewed_by_id, rejection_reason=model.rejection_reason,
            reviewed_at=model.reviewed_at, created_at=model.created_at
        )

    def save(self, product: GlobalProduct) -> GlobalProduct:
        model = GlobalProductModel(
            id=product.id, name=product.name, category_id=product.category_id,
            scientific_name=product.scientific_name, synonyms=product.synonyms,
            taxonomy_code=product.taxonomy_code, ncm_code=product.ncm_code,
            description_template=product.description_template, image_url=product.image_url,
            status=product.status, suggested_by_id=product.suggested_by_id,
            reviewed_by_id=product.reviewed_by_id, rejection_reason=product.rejection_reason,
            reviewed_at=product.reviewed_at, created_at=product.created_at
        )
        self.db.merge(model)
        self.db.commit()
        return product

    def get_by_id(self, product_id: UUID) -> Optional[GlobalProduct]:
        model = self.db.query(GlobalProductModel).filter(GlobalProductModel.id == product_id).first()
        return self._to_domain(model) if model else None

    def get_by_name(self, name: str) -> Optional[GlobalProduct]:
        model = self.db.query(GlobalProductModel).filter(GlobalProductModel.name == name).first()
        return self._to_domain(model) if model else None

    def get_all_by_status(self, status: ProductStatus, skip: int = 0, limit: int = 100) -> List[GlobalProduct]:
        models = self.db.query(GlobalProductModel).filter(GlobalProductModel.status == status).offset(skip).limit(limit).all()
        return [self._to_domain(m) for m in models]

    def get_by_category(self, category_id: UUID, skip: int = 0, limit: int = 100) -> List[GlobalProduct]:
        models = self.db.query(GlobalProductModel).filter(
            GlobalProductModel.category_id == category_id,
            GlobalProductModel.status == ProductStatus.APPROVED
        ).offset(skip).limit(limit).all()
        return [self._to_domain(m) for m in models]
    
    def search_by_text(self, query: str, skip: int = 0, limit: int = 100) -> List[GlobalProduct]:
        search_term = f"%{query}%"
        models = self.db.query(GlobalProductModel).filter(
            GlobalProductModel.status == ProductStatus.APPROVED,
            or_(
                GlobalProductModel.name.ilike(search_term),
                GlobalProductModel.synonyms.ilike(search_term)
            )
        ).offset(skip).limit(limit).all()
        return [self._to_domain(m) for m in models]