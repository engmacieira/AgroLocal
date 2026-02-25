# 🤖 Contexto de Continuidade: AgroLocal

> **PARA O AGENTE/DESENVOLVEDOR (MARK):**
> Este arquivo é o seu Ponto de Restauração. Antes de processar qualquer novo prompt, analise este estado para garantir consistência com a sessão anterior.

## 📍 Estado Atual da Missão
* **Fase do Projeto:** Desenvolvimento (Sprint 09).
* **Sprint Atual:** Sprint 09 - Sistema de Avaliações (`Review`).
* **Última Ação Realizada:** Finalizamos 100% da Sprint 08. O motor de Repasses (`Payout`) está completo, incluindo o cálculo da "Platform Fee" (comissão), agendamento e o processamento que finaliza o pedido (`COMPLETED`). 
* **PRÓXIMO PASSO IMEDIATO:** Planejar e executar o backlog da Sprint 09 (Entidade `Review`). Criar as regras de domínio garantindo que o cliente só avalia pedidos entregues, com notas entre 1 e 5 estrelas.

## 🏗️ Definições Arquiteturais (Não Quebrar)
* **Backend:** Python (FastAPI) + SQLAlchemy + DDD estrito.
* **Dinheiro:** Sempre usar `Decimal` para valores, taxas e totais.
* **Testes:** TDD é obrigatório (Red-Green-Refactor).

## 🧭 Mapa da Verdade (Onde buscar detalhes)
* **Logs anteriores:** Consulte os arquivos concluídos na pasta `docs/sprint/`.

---
*Atualizado em: 25/02/2026*