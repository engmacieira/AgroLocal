# 🗺️ Sprint 01: Fundação e Modelagem de Dados

**Objetivo:** Estabelecer a arquitetura base do projeto (Backend e Frontend), configurar o ambiente de desenvolvimento e implementar a modelagem de dados relacional para suportar o cadastro de usuários e produtos.
**Status:** Planejamento
**Tecnologia Principal:** FastAPI, SQLAlchemy, Alembic, React Native (Expo).

---

## 🎯 Backlog de Funcionalidades (Escopo)
*Foco total na infraestrutura para suportar as User Stories [US-01] a [US-04].*

### 📦 1. Infraestrutura e Setup
* **[TECH-01] Setup Inicial do Projeto (Monorepo Híbrido)**
    * **O que é:** Execução do script de setup para criar a estrutura de pastas padrão.
    * **Critério de Aceite:**
        * Backend rodando com `uvicorn` (Health Check OK).
        * Frontend Mobile iniciado com `npx create-expo-app` (TypeScript).
        * Repositório Git iniciado com `.gitignore` correto.

* **[TECH-02] Configuração do Banco de Dados e Migrations**
    * **O que é:** Configurar SQLAlchemy (Engine/Session) e inicializar o Alembic.
    * **Critério de Aceite:**
        * Arquivo `alembic.ini` configurado.
        * Comando `alembic revision --autogenerate` funcionando.

### 📦 2. Modelagem de Dados (Backend)
* **[DB-01] Tabela de Usuários e Autenticação (Base)**
    * **O que é:** Criar o model `User` (email, senha hash, role, timestamps).
    * **Regra de Negócio:** O campo `role` deve distinguir entre 'ADMIN', 'PRODUTOR' e 'CONSUMIDOR'.

* **[DB-02] Perfis de Usuário (1:1)**
    * **O que é:** Criar tabelas `ProducerProfile` (CPF, Pix, Bio, Localização) e `ConsumerProfile` (Telefone).
    * **Regra de Negócio:** Um usuário só pode ter um perfil ativo por vez (ou estrutura polimórfica).

* **[DB-03] Catálogo e Ofertas (1:N)**
    * **O que é:** Criar models `Product` (Nome base, Categoria) e `Offer` (Preço, Qtd, Tipo de Entrega, Vínculo com Produtor).
    * **Regra de Negócio:** A oferta deve ter enum para o tipo de disponibilidade (PRONTA_ENTREGA, ENCOMENDA).

### 📦 3. Camada de Validação (Schemas)
* **[API-01] Schemas Pydantic (Input/Output)**
    * **O que é:** Criar os DTOs para criação e leitura dos models acima.
    * **Critério de Aceite:** Validação de CPF e formato de Email nos schemas de entrada.

---

## 🛠️ Plano Técnico de Execução
*Passo a passo para o desenvolvedor (Mark & Matheus).*

1.  **Setup:** Rodar o `setup.py` (ajustado para incluir pasta `mobile` ao invés de `frontend` web se preferirmos, ou manter ambos).
2.  **Database Core:** Criar `app/core/database.py` e `app/core/config.py`.
3.  **Models:** Criar arquivos em `app/models/`:
    * `user_model.py`
    * `profile_model.py`
    * `product_model.py`
4.  **Alembic:** Configurar `env.py` para importar todos os models (evitar erro de "no changes detected").
5.  **Migration 01:** Gerar e aplicar a primeira migração.
6.  **Schemas:** Criar os espelhos dos models em `app/schemas/`.

---

## 📝 Definição de Pronto (DoD)
*Checklist para considerar a Sprint finalizada.*

* [ ] Estrutura de pastas criada.
* [ ] Models criados e revisados.
* [ ] Migration inicial aplicada no banco SQLite (dev).
* [ ] Diagrama ER (mental ou documentado) validado.
* [ ] Nenhuma rota de API precisa estar funcional ainda, apenas a estrutura de dados.