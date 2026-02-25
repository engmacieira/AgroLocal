from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.infrastructure.repositories.catalog_repository_impl import CategoryRepositoryImpl, GlobalProductRepositoryImpl
from app.application.use_cases.catalog_management import (
    CreateCategoryUseCase, SuggestProductUseCase, SuggestProductDTO,
    ApproveProductUseCase, RejectProductUseCase, GetProductsByCategoryUseCase, GetProductsByStatusUseCase
)
from app.presentation.schemas.catalog_schema import (
    CategoryCreateRequest, CategoryResponse,
    ProductSuggestRequest, ProductResponse, ProductRejectRequest, ProductStatus
)

router = APIRouter(prefix="/catalog", tags=["Catalog"])

# --- Rotas de Categoria ---

@router.post("/categories/", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(request: CategoryCreateRequest, db: Session = Depends(get_db)):
    repo = CategoryRepositoryImpl(db)
    use_case = CreateCategoryUseCase(repo)
    try:
        return use_case.execute(name=request.name, icon_url=request.icon_url)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/categories/", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    repo = CategoryRepositoryImpl(db)
    return repo.get_all_active()

# --- Rotas de Produto Global ---

@router.post("/products/suggest", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def suggest_product(request: ProductSuggestRequest, db: Session = Depends(get_db)):
    cat_repo = CategoryRepositoryImpl(db)
    prod_repo = GlobalProductRepositoryImpl(db)
    use_case = SuggestProductUseCase(prod_repo, cat_repo)
    
    dto = SuggestProductDTO(**request.model_dump())
    try:
        return use_case.execute(dto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.patch("/products/{product_id}/approve", response_model=ProductResponse)
def approve_product(product_id: UUID, admin_id: UUID, db: Session = Depends(get_db)):
    repo = GlobalProductRepositoryImpl(db)
    use_case = ApproveProductUseCase(repo)
    try:
        return use_case.execute(product_id=product_id, admin_id=admin_id)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.patch("/products/{product_id}/reject", response_model=ProductResponse)
def reject_product(product_id: UUID, request: ProductRejectRequest, db: Session = Depends(get_db)):
    repo = GlobalProductRepositoryImpl(db)
    use_case = RejectProductUseCase(repo)
    try:
        return use_case.execute(product_id=product_id, admin_id=request.admin_id, reason=request.reason)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    
@router.get("/categories/{category_id}/products", response_model=List[ProductResponse])
def get_products_by_category(category_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista produtos APROVADOS de uma categoria específica (Vitrine para o Produtor)."""
    repo = GlobalProductRepositoryImpl(db)
    use_case = GetProductsByCategoryUseCase(repo)
    return use_case.execute(category_id, skip, limit)

@router.get("/products/status/{status}", response_model=List[ProductResponse])
def get_products_by_status(status: ProductStatus, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista produtos por status (Ex: PENDING para a fila de moderação do Admin)."""
    repo = GlobalProductRepositoryImpl(db)
    use_case = GetProductsByStatusUseCase(repo)
    return use_case.execute(status, skip, limit)