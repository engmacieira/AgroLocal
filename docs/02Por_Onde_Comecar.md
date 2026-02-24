# 🤖 Contexto de Continuidade: AgroLocal

> **PARA O AGENTE/DESENVOLVEDOR (MARK):**
> Este arquivo é o seu Ponto de Restauração. Antes de processar qualquer novo prompt, analise este estado para garantir consistência com a sessão anterior.

## 📍 Estado Atual da Missão
* **Fase do Projeto:** Desenvolvimento (Sprint 02).
* **Sprint Atual:** Sprint 02 - Gestão de Endereços (Address).
* **Última Ação Realizada:** Finalizamos 100% da Entidade `User` com arquitetura DDD, TDD verde, e autenticação JWT. O repositório e testes base já estão maduros (`conftest.py` configurado).
* **PRÓXIMO PASSO IMEDIATO:** Criar o arquivo `app/tests/domain/test_address.py` e escrever o primeiro teste RED para as regras de negócio da entidade `Address` (ex: vincular a um `User`, validar CEP).

## 🏗️ Definições Arquiteturais (Não Quebrar)
* **Backend:** Python (FastAPI) + SQLAlchemy + Alembic.
    * *Regra:* DDD estrito. O Domínio não conhece o SQLAlchemy.
    * *Banco:* SQLite (Dev) compatível com PostgreSQL (Prod) via classe `GUID` (`app/core/database.py`).
    * *Segurança:* JWT + Bcrypt configurados em `app/core/security.py`.
* **Testes:** TDD é obrigatório. Fixtures globais estão no `app/tests/conftest.py`.

## 🧭 Mapa da Verdade (Onde buscar detalhes)
* **O que fazer (Escopo):** Consulte a sequência lógica de entidades discutida.
* **Histórico:** Consulte `docs/sprint/sprint_01_conclusao.md` para ver as fundações da Sprint 1.

---
*Atualizado em: 24/02/2026*