# 🏁 Log de Sprint: 02 - Qualidade, Validação e Seeds

**Período:** 18/02/2026
**Status:** Concluído
**Foco:** Blindagem da aplicação com Schemas Pydantic rigorosos, Scripts de Povoamento (Seed) e Testes Automatizados.

## 🚀 Entregas Realizadas (O Que)
* **[Schemas]** Refatoração completa de todas as camadas de entrada/saída (DTOs) com Pydantic.
    * Aplicação de `Regex` para CPFs, CNPJs, NCMs e URLs.
    * Adição de exemplos ricos (`ConfigDict`) para gerar documentação Swagger/OpenAPI detalhada.
    * Validações de negócio (ex: preço > 0, datas válidas, coordenadas geográficas).
* **[Scripts]** Criação do `scripts/seeds.py` capaz de povoar o banco PostgreSQL com dados complexos e relacionais, respeitando a integridade dos UUIDs.
* **[Testes]** Configuração do ambiente `pytest` com banco em memória (SQLite).
    * Criação de `test_models.py` (Integridade do Banco).
    * Criação de `test_schemas.py` (Validação de entrada).
    * Criação de `test_domain_schemas.py` (Regras de Negócio complexas).
* **[Infra]** Ajustes no `requirements.txt` com novas dependências de validação (`email-validator`) e segurança preliminar.

## 🧠 Retrospectiva (O Como)
### ✅ O que funcionou bem?
* **Pydantic V2:** O uso de `Field` com constraints (`gt`, `le`, `pattern`) reduziu drasticamente a necessidade de escrever validadores manuais (if/else).
* **Seeding:** O script de população provou ser essencial para validar se as Foreign Keys (UUID) estavam se comportando corretamente antes de plugar o Frontend.
* **Testes de Schema:** Detectaram erros de arredondamento financeiro (3 casas decimais) antes que eles se tornassem bugs de produção.

### ⚠️ Lições Aprendidas / Obstáculos
* **Configuração do Pytest:** Foi necessário ajustar o `pytest.ini` (`pythonpath = .`) e o `conftest.py` (importação explícita de todos os models) para que o SQLAlchemy encontrasse os relacionamentos no ambiente de teste.
* **Dependências Ocultas:** O Pydantic requer a instalação explícita de `pydantic[email]` para validar o tipo `EmailStr`.

---

## 📊 Status Final
* **Cobertura de Testes:** Alta nas camadas de Model e Schema.
* **Documentação:** Swagger UI (Docs) agora possui exemplos reais para todas as rotas (User, Product, Order, etc).
* **Próximos Passos:** Iniciar a **Sprint 03** focada em Autenticação (Login, JWT, Hash de Senha) e Proteção de Rotas.