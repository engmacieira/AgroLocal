# 🗺️ Sprint 02: Validação, Qualidade e Massa de Dados

**Objetivo:** Garantir a integridade dos dados através de Schemas Pydantic, implementar a base de testes automatizados e criar um ambiente de desenvolvimento rico com dados semeados (Seeds).
**Status:** Planejamento
**Tecnologia Principal:** FastAPI (Pydantic), Pytest, SQLAlchemy.

---

## 🎯 Backlog de Funcionalidades (Escopo)
*Foco na robustez técnica e produtividade do desenvolvedor.*

### 📦 1. Camada de Validação (Schemas)
* **[TECH-03] Schemas Pydantic de Domínio**
    * **O que é:** Criar os modelos Pydantic (Input/Output/Update) para todas as entidades (User, Product, Order, etc.).
    * **Critério de Aceite:**
        * Atributos batendo com os Models (UUID, Numeric, Enums).
        * Validações extras (Ex: CPF, Email, Chave PIX).
        * Herança de BaseSchema para evitar repetição de código.

### 📦 2. Garantia de Qualidade (Testes)
* **[TECH-04] Suíte de Testes Automatizados (Base)**
    * **O que é:** Implementar testes de unidade usando Pytest para as pastas `core`, `models` e `schemas`.
    * **Critério de Aceite:**
        * Testar conexão com banco e carregamento de `settings` (`core`).
        * Testar criação de instâncias de modelos e validação de relacionamentos (`models`).
        * Testar inputs válidos e inválidos nos schemas (`schemas`).

### 📦 3. Utilitários de Desenvolvimento (Seed)
* **[TECH-05] Script de Povoamento (Seeding)**
    * **O que é:** Criar um script para popular o PostgreSQL com dados iniciais e de teste.
    * **Critério de Aceite:**
        * Inserção de Categorias globais (Frutas, Legumes, etc.).
        * Inserção de Produtos Globais aprovados.
        * Criação de Usuários (Admin, Produtor e Cliente) de teste.

---

## 🛠️ Plano Técnico de Execução
*O passo a passo para o desenvolvedor (Mark & Matheus).*

1.  **Setup de Testes:** * Configurar `pytest.ini` e `conftest.py` para isolar o banco de testes.
2.  **Desenvolvimento de Schemas:** * Criar `app/schemas/base_schema.py` com mixins comuns (id, created_at).
    * Criar subpastas para organizar (auth, products, orders).
3.  **Implementação de Seeds:**
    * Criar `app/core/seeds.py` usando a `SessionLocal` para inserir dados básicos.
4.  **Execução de Testes:**
    * Validar que as regras de `CheckConstraint` (como a nota do review 1-5) estão funcionando.

---

## 📝 Definição de Pronto (DoD)
*Checklist para considerar a Sprint finalizada.*

* [ ] Todos os Schemas mapeados para as tabelas atuais.
* [ ] Cobertura de teste inicial para os componentes críticos do `core`.
* [ ] Banco de dados populado com sucesso via script (sem erros de FK).
* [ ] Documentação de Dívidas Técnicas atualizada, se houver.