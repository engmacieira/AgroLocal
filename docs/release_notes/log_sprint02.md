feat(sprint-02): finaliza schemas pydantic, script de seed e testes automatizados

Conclui o escopo da Sprint 02 focada na integridade, validação e qualidade dos dados.

Alterações principais:

1. Refatoração de Schemas (Pydantic V2):
   - Implementada validação rigorosa com Regex (CPF, CNPJ, NCM) e limites numéricos (preço > 0, lat/long).
   - Adicionados exemplos ricos (`ConfigDict`) em todos os schemas para gerar documentação Swagger/OpenAPI detalhada.
   - Mapeamento completo dos domínios: User, Product, Order, Transaction, Payout, Review, Address, Audit e Catalog.

2. Testes Automatizados (Pytest):
   - Configurado ambiente de teste com banco SQLite em memória (`conftest.py`).
   - Criados testes de unidade para Models (`test_models.py`) validando UUIDs e Constraints.
   - Criados testes de validação (`test_schemas.py` e `test_domain_schemas.py`) para garantir regras de negócio.

3. Infraestrutura e Scripts:
   - Criado script `scripts/seeds.py` para povoamento inicial do banco com dados complexos e relacionais.
   - Ajustado `pytest.ini` para reconhecimento correto dos módulos.
   - Atualizado `requirements.txt` com novas dependências (`email-validator`, `passlib`, `python-jose`).

4. Documentação:
   - Gerado log de conclusão da Sprint 02 (`docs/sprint/SPRINT_02_CONCLUSAO.md`).

Refs: #Sprint02