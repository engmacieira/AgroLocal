# 🤖 Contexto de Continuidade: AgroLocal

> **PARA O AGENTE/DESENVOLVEDOR (MARK):**
> Este arquivo é o seu Ponto de Restauração. Antes de processar qualquer novo prompt, analise este estado para garantir consistência com a sessão anterior.

## 📍 Estado Atual da Missão
* **Fase do Projeto:** Desenvolvimento (Sprint 04).
* **Sprint Atual:** Sprint 04 - Gestão de Produtos (`ProducerProduct`).
* **Última Ação Realizada:** Finalizamos 100% da Entidade `ProducerProfile` (Vendedor), garantindo relação 1:1 com `User` e protegendo dados como CNPJ/CPF e PIX.
* **PRÓXIMO PASSO IMEDIATO:** Planejar o backlog da Sprint 04 e criar o primeiro teste RED de Domínio para a entidade de Produtos. O produto deve pertencer a um `ProducerProfile` (FK), ter preço, estoque, categoria, e unidade de medida (Kg, Unidade, Maço).

## 🏗️ Definições Arquiteturais (Não Quebrar)
* **Backend:** Python (FastAPI) + SQLAlchemy + DDD estrito.
* **Testes:** TDD é obrigatório (Red-Green-Refactor). Fixtures globais estão no `app/tests/conftest.py`.

## 🧭 Mapa da Verdade (Onde buscar detalhes)
* **Logs anteriores:** Consulte `docs/sprint/sprint_01_conclusao.md`, `02` e `03_conclusao.md`.

---
*Atualizado em: 24/02/2026*