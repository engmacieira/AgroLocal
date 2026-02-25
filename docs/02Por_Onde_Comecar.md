# 🤖 Contexto de Continuidade: AgroLocal

> **PARA O AGENTE/DESENVOLVEDOR (MARK):**
> Este arquivo é o seu Ponto de Restauração. Antes de processar qualquer novo prompt, analise este estado para garantir consistência com a sessão anterior.

## 📍 Estado Atual da Missão
* **Fase do Projeto:** Desenvolvimento (Sprint 05).
* **Sprint Atual:** Sprint 05 - Ofertas e Prateleira (`ProducerProduct`).
* **Última Ação Realizada:** Finalizamos 100% da Sprint 04 (Catálogo Global e Categorias), com moderação de produtos via status (PENDING/APPROVED).
* **PRÓXIMO PASSO IMEDIATO:** Planejar o backlog da Sprint 05 e resgatar o teste RED de Domínio para a entidade `ProducerProduct` (Oferta). Precisamos vincular o `ProducerProfile` ao `GlobalProduct`, definindo preço (maior que zero), estoque (não negativo), unidade de medida e tipo de disponibilidade (Pronta Entrega/Encomenda).

## 🏗️ Definições Arquiteturais (Não Quebrar)
* **Backend:** Python (FastAPI) + SQLAlchemy + DDD estrito.
* **Testes:** TDD é obrigatório (Red-Green-Refactor). Fixtures globais estão no `app/tests/conftest.py`.

## 🧭 Mapa da Verdade (Onde buscar detalhes)
* **Logs anteriores:** Consulte os arquivos concluídos na pasta `docs/sprint/`.

---
*Atualizado em: 24/02/2026*