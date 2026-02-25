# 🤖 Contexto de Continuidade: AgroLocal

> **PARA O AGENTE/DESENVOLVEDOR (MARK):**
> Este arquivo é o seu Ponto de Restauração. Antes de processar qualquer novo prompt, analise este estado para garantir consistência com a sessão anterior.

## 📍 Estado Atual da Missão
* **Fase do Projeto:** Desenvolvimento (Sprint 07).
* **Sprint Atual:** Sprint 07 - Financeiro (Pagamentos/Repasses) e Avaliações (`Transaction`, `Payout`, `Review`).
* **Última Ação Realizada:** Finalizamos 100% da Sprint 06. O sistema agora processa carrinhos de compras (Checkout), faz o split de pedidos por produtor, calcula o frete de maior valor, deduz o estoque, gera o Snapshot Fiscal (OrderItem) e gerencia a máquina de estados (CREATED -> PAID -> PREPARING -> READY -> DELIVERED).
* **PRÓXIMO PASSO IMEDIATO:** Planejar o backlog da Sprint 07. Como rascunhado no modelo antigo do pedido, precisamos vincular o pedido pago a uma transação financeira (`Transaction`), calcular a taxa da plataforma (Split de Pagamento), preparar o repasse para o produtor (`Payout`) e permitir que o cliente deixe uma avaliação (`Review`) após a entrega.

## 🏗️ Definições Arquiteturais (Não Quebrar)
* **Backend:** Python (FastAPI) + SQLAlchemy + DDD estrito.
* **Dinheiro:** Sempre usar `Decimal` para valores, taxas e totais.
* **Testes:** TDD é obrigatório (Red-Green-Refactor).

## 🧭 Mapa da Verdade (Onde buscar detalhes)
* **Logs anteriores:** Consulte os arquivos concluídos na pasta `docs/sprint/`.

---
*Atualizado em: 25/02/2026*