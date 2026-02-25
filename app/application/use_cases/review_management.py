import uuid
from typing import Optional
from app.domain.entities.review import Review
from app.domain.repositories.review_repository import IReviewRepository
from app.domain.repositories.order_repository import IOrderRepository

class CreateReviewUseCase:
    """Caso de Uso: Permite que um cliente avalie um pedido já entregue."""
    def __init__(self, review_repository: IReviewRepository, order_repository: IOrderRepository):
        self.review_repository = review_repository
        self.order_repository = order_repository

    def execute(self, order_id: uuid.UUID, customer_id: uuid.UUID, rating: int, comment: Optional[str] = None, photo_url: Optional[str] = None) -> Review:
        # 1. Busca e Valida a Ordem
        pedido = self.order_repository.get_by_id(order_id)
        if not pedido:
            raise ValueError("Pedido não encontrado")

        # 2. Valida a Autoria (Apenas o comprador pode avaliar)
        if pedido.customer_id != customer_id:
            raise ValueError("Você só pode avaliar os seus próprios pedidos")

        # 3. Valida o Status (Só avalia o que já recebeu)
        if pedido.status not in ["DELIVERED", "COMPLETED"]:
            raise ValueError("Apenas pedidos entregues ou concluídos podem ser avaliados")

        # 4. Valida a Regra 1:1 (Evita Spam de avaliações no mesmo pedido)
        avaliacao_existente = self.review_repository.get_by_order_id(order_id)
        if avaliacao_existente:
            raise ValueError("Este pedido já foi avaliado anteriormente")

        # 5. Cria e Salva a Entidade
        nova_avaliacao = Review(
            order_id=pedido.id,
            customer_id=pedido.customer_id,
            producer_id=pedido.producer_id,
            rating=rating,
            comment=comment,
            photo_url=photo_url
        )

        return self.review_repository.save(nova_avaliacao)