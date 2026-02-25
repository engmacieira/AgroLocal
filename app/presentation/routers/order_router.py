from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID

from app.core.database import get_db
from app.infrastructure.repositories.order_repository_impl import OrderRepositoryImpl
from app.infrastructure.repositories.producer_product_repository_impl import ProducerProductRepositoryImpl
from app.infrastructure.repositories.catalog_repository_impl import GlobalProductRepositoryImpl

from app.application.use_cases.checkout_management import (
    CheckoutUseCase, CheckoutCartDTO, CheckoutProducerGroupDTO, CheckoutItemDTO,
    UpdateOrderStatusUseCase
)
from app.presentation.schemas.order_schema import CheckoutCartRequest, OrderResponse, OrderStatusUpdateRequest

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/checkout", response_model=List[OrderResponse], status_code=status.HTTP_201_CREATED)
def checkout(request: CheckoutCartRequest, db: Session = Depends(get_db)):
    """
    Processa um carrinho de compras.
    Gera um pedido (Order) separado para cada produtor, calculando o frete máximo e reservando estoque.
    """
    order_repo = OrderRepositoryImpl(db)
    offer_repo = ProducerProductRepositoryImpl(db)
    catalog_repo = GlobalProductRepositoryImpl(db)
    
    use_case = CheckoutUseCase(order_repo, offer_repo, catalog_repo)
    
    # Mapeando Request Schema para DTO
    groups_dto = [
        CheckoutProducerGroupDTO(
            producer_id=g.producer_id,
            delivery_type=g.delivery_type,
            items=[CheckoutItemDTO(offer_id=i.offer_id, quantity=i.quantity) for i in g.items]
        )
        for g in request.groups
    ]
    cart_dto = CheckoutCartDTO(customer_id=request.customer_id, groups=groups_dto)
    
    try:
        pedidos_gerados = use_case.execute(cart_dto)
        return pedidos_gerados
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/customer/{customer_id}", response_model=List[OrderResponse])
def get_customer_orders(customer_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista o histórico de compras de um cliente."""
    repo = OrderRepositoryImpl(db)
    return repo.get_by_customer_id(customer_id, skip, limit)

@router.get("/producer/{producer_id}", response_model=List[OrderResponse])
def get_producer_orders(producer_id: UUID, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Lista os pedidos recebidos por um produtor (Painel de Vendas)."""
    repo = OrderRepositoryImpl(db)
    return repo.get_by_producer_id(producer_id, skip, limit)

@router.patch("/{order_id}/status", response_model=OrderResponse)
def update_order_status(order_id: UUID, request: OrderStatusUpdateRequest, db: Session = Depends(get_db)):
    """Atualiza o status do pedido (Máquina de Estados)."""
    repo = OrderRepositoryImpl(db)
    use_case = UpdateOrderStatusUseCase(repo)
    
    try:
        return use_case.execute(order_id, request.action.value, request.reason)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))