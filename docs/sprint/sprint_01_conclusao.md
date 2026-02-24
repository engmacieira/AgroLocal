# 🏁 Log de Sprint: 01 - Fundação DDD e Entidade User

**Período:** 24/02/2026
**Status:** Concluído
**Foco:** Estruturar a base da arquitetura DDD, configurar o banco de dados híbrido e entregar a fatia vertical completa (CRUD + Auth) da Entidade `User`.

## 🚀 Entregas Realizadas (O Que)
* **[Infra]** Implementação do `database.py` com suporte híbrido (PostgreSQL/SQLite) usando a classe customizada `GUID`.
* **[Infra]** Refatoração da infraestrutura de testes com `conftest.py`, garantindo princípio DRY e usando `StaticPool` para manter o SQLite em memória vivo durante a sessão.
* **[Backend]** Construção da Entidade Rica `User` protegendo regras de negócio (Soft Delete, Aceite de Termos, Verificação).
* **[Backend]** Criação do Repositório SQLAlchemy implementando o Contrato de Domínio (`IUserRepository`).
* **[Backend]** Implementação de Casos de Uso para Registro, Atualização, Deleção e Segurança (JWT + Bcrypt).
* **[Apresentação]** Criação de Rotas no FastAPI protegidas por Schemas Pydantic (V2).
* **[Qualidade]** 100% de cobertura de testes da entidade `User` (Red-Green-Refactor concluído com sucesso).

## 🧠 Retrospectiva (O Como)
### ✅ O que funcionou bem?
* A abordagem de fatias verticais com TDD provou ser excelente. Os testes E2E na camada de rotas capturaram problemas de Schema imediatamente.
* A divisão de responsabilidades (Domínio puro vs Infraestrutura) está mantendo o código altamente legível.

### ⚠️ Lições Aprendidas / Obstáculos
* **Bug do banco em memória:** O SQLite resetava a cada chamada, resolvido aplicando `StaticPool` na engine de testes.
* **Limitação do Bcrypt 4.1.0+:** Incompatibilidade nativa com o `passlib` gerou um limite de 72 bytes incorreto nos testes. Contornado via downgrade do bcrypt para `4.0.1`.
* **Rollback de Testes:** Aprendemos que a limpeza do banco entre os testes via transação exige que cada teste que dependa de estado prepare seu próprio *Arrange* (ex: teste de e-mail duplicado).

---

## 📊 Status Final
* **Dívidas Técnicas Geradas:** Adicionar os *scopes/roles* dentro do payload do JWT futuramente para autorização de rotas (ex: separar admin de cliente).
* **Próximos Passos:** Iniciar a Sprint 02 focada na Entidade `Address`.

---
**Assinatura:** Mark Construtor & Matheus