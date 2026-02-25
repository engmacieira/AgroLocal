# 🏁 Log de Sprint: 06 - Carrinho Inteligente e Gestão de Pedidos

**Período:** 25/02/2026
**Status:** Concluído
**Foco:** Implementar o motor de Checkout (Carrinho) e a entidade `Order`, com suporte a divisão de pedidos por produtor, cálculo de frete máximo, reserva de estoque e máquina de estados.

## 🚀 Entregas Realizadas (O Que)
* **[Domínio]** Criação da entidade `Order` e `OrderItem` (Snapshot Fiscal Imutável). Implementação da máquina de estados (`OrderStatus`): `CREATED` -> `PAID` -> `PREPARING` -> `READY` -> `DELIVERED`, com suporte a `CANCELED` (exigindo justificativa).
* **[Infra]** Modelos `OrderModel` e `OrderItemModel` no SQLAlchemy, utilizando `Numeric` para precisão financeira e `cascade="all, delete-orphan"` para garantir a integridade do pedido.
* **[Aplicação]** Criação do poderoso orquestrador `CheckoutUseCase` que processa o carrinho, separa itens por produtor, aplica a regra do "Frete Maior", deduz o estoque em tempo real e captura o nome real do produto no Catálogo Global. Criação do `UpdateOrderStatusUseCase` para o pós-venda.
* **[Apresentação]** Schemas rigorosos Pydantic (`gt=0` para quantidades). Rotas `/orders/checkout` e `/orders/{order_id}/status`.
* **[Qualidade]** 100% de cobertura E2E. Testes validando a jornada completa: desde o registro dos usuários, criação das vitrines, até a compra de múltiplos itens, deduções de estoque e avanço até a entrega do pedido.

## 🧠 Retrospectiva (O Como)
### ✅ O que funcionou bem?
* **Padrão DTO no Checkout:** O uso de DTOs estruturados (`CheckoutCartDTO`, `CheckoutProducerGroupDTO`) tornou o Caso de Uso de Checkout limpo, separando perfeitamente a lógica de negócio do payload recebido da web.
* **Snapshot Fiscal:** Copiar dados como `product_name_snapshot` e `unit_price_snapshot` no momento da compra blindou o histórico do cliente contra alterações futuras feitas pelo produtor.

### ⚠️ Lições Aprendidas / Obstáculos
* **Atenção ao Pydantic:** Validações de domínio que falham logo no cadastro (como a senha mínima de 6 caracteres do usuário) podem mascarar erros em testes E2E complexos. A validação de entrada sempre age antes da lógica de negócios.

---

## 📊 Status Final
* **Próximos Passos:** Iniciar a Sprint 07 focada no Financeiro e Avaliações (`Transaction`, `Payout` e `Review`). Agora que os pedidos são criados e entregues, precisamos gerenciar o pagamento e permitir que o cliente avalie a qualidade do produtor.

---
**Assinatura:** Mark Construtor & Matheus