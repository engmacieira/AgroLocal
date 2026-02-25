# 🤖 Contexto de Continuidade: AgroLocal

> **PARA O AGENTE/DESENVOLVEDOR (MARK):**
> Este arquivo é o seu Ponto de Restauração. Antes de processar qualquer novo prompt, analise este estado para garantir consistência com a sessão anterior.

## 📍 Estado Atual da Missão
* **Fase do Projeto:** Desenvolvimento (Sprint 08).
* **Sprint Atual:** Sprint 08 - Repasses Financeiros (`Payout`) e Avaliações (`Review`).
* **Última Ação Realizada:** Finalizamos 100% da Sprint 07 (Inflow). O sistema agora agrupa múltiplos pedidos numa única Transação, gera o PIX unificado e processa Webhooks de aprovação que alteram o status dos pedidos para PAID em cascata.
* **PRÓXIMO PASSO IMEDIATO:** Planejar o backlog da Sprint 08. Modelar a entidade `Payout` (Repasse), que vai calcular a "Platform Fee" (comissão do AgroLocal) e definir o valor líquido a ser transferido para o produtor após a venda. Na sequência, modelar a entidade `Review` para o cliente avaliar o pedido entregue.

## 🏗️ Definições Arquiteturais (Não Quebrar)
* **Backend:** Python (FastAPI) + SQLAlchemy + DDD estrito.
* **Dinheiro:** Sempre usar `Decimal` para valores, taxas e totais.
* **Testes:** TDD é obrigatório (Red-Green-Refactor).

## 🧭 Mapa da Verdade (Onde buscar detalhes)
* **Logs anteriores:** Consulte os arquivos concluídos na pasta `docs/sprint/`.

---
*Atualizado em: 25/02/2026*