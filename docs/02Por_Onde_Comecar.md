# 🤖 Contexto de Continuidade: AgroLocal

> **PARA O AGENTE/DESENVOLVEDOR (MARK):**
> Este arquivo é o seu Ponto de Restauração. Antes de processar qualquer novo prompt, analise este estado para garantir consistência com a sessão anterior.

## 📍 Estado Atual da Missão
* **Fase do Projeto:** Desenvolvimento (Sprint 03).
* **Sprint Atual:** Sprint 03 - Cadastro de Produtor / Vendedor (`ProducerProfile`).
* **Última Ação Realizada:** Finalizamos 100% da Entidade `Address` (Endereços) com foco em logística rural, com testes cobrindo todas as fatias verticais.
* **PRÓXIMO PASSO IMEDIATO:** Criar a base de testes de Domínio para a nova entidade `ProducerProfile`. O perfil de produtor deve estar vinculado a um `User` (FK) e conter dados de negócio como CNPJ/CPF, nome da lojinha, chave PIX e avaliações.

## 🏗️ Definições Arquiteturais (Não Quebrar)
* **Backend:** Python (FastAPI) + SQLAlchemy + DDD estrito.
* **Testes:** TDD é obrigatório (Red-Green-Refactor). Fixtures globais estão no `app/tests/conftest.py`.

## 🧭 Mapa da Verdade (Onde buscar detalhes)
* **Logs anteriores:** Consulte `docs/sprint/sprint_01_conclusao.md` e `sprint_02_conclusao.md`.

---
*Atualizado em: 24/02/2026*