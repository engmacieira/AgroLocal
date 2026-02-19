# 🗺️ Sprint 03: Backend - Segurança e Autenticação Real

**Objetivo:** Implementar o "Coração da Segurança" do AgroLocal. Substituir o Login Mock por um sistema real de JWT, Hash de Senha e Persistência no PostgreSQL.
**Responsável:** Backend Dev (Matheus)
**Status:** A Fazer

---

## 🔐 1. Core de Segurança (Security)
* **[SEC-01] Utilitários de Criptografia**
    * **Arquivo:** `app/core/security.py`
    * **Tarefa:** Configurar `passlib` para hash de senha (Bcrypt) e `python-jose` para geração de tokens.
    * **Critério:** Funções `verify_password`, `get_password_hash` e `create_access_token` funcionando com testes unitários.

* **[SEC-02] Dependência de Injeção de Usuário**
    * **Arquivo:** `app/api/deps.py`
    * **Tarefa:** Criar a função `get_current_user` que valida o Token JWT no header `Authorization: Bearer ...`.
    * **Critério:** Se o token for inválido ou expirado, deve retornar erro 401 automaticamente.

## 👤 2. Rotas de Autenticação (Real)
* **[API-02] Router de Login (OAuth2)**
    * **Rota:** `POST /api/v1/auth/login`
    * **Tarefa:** Receber email/senha, validar no banco e retornar o Access Token real.
    * **Diferença do Mock:** Deve buscar o usuário no banco PostgreSQL e verificar o hash da senha.

* **[API-03] Router de Cadastro (Sign Up)**
    * **Rota:** `POST /api/v1/users/signup`
    * **Schema:** `UserCreate` (Já criado na Sprint 02).
    * **Tarefa:** Criar usuário no banco. Se tiver `producer_profile` no payload, criar o perfil atomicamente (Transaction).
    * **Validação:** Garantir que não duplique E-mail, CPF ou CNPJ.

## 🧱 3. Rotas de Usuário (Protegidas)
* **[API-04] Perfil do Usuário Logado**
    * **Rota:** `GET /api/v1/users/me`
    * **Tarefa:** Usar a dependência `get_current_user` para retornar os dados do usuário que chamou a API.
    * **Objetivo:** Substituir a rota `/mocks/users/me` pela versão que consulta o banco.

---

## 📝 Definição de Pronto (DoD Backend)
* [ ] Login gera um JWT válido que expira no tempo configurado.
* [ ] Senhas no banco estão encriptadas (nunca texto puro).
* [ ] É possível criar um usuário novo e logar com ele imediatamente.
* [ ] Testes de integração para o fluxo de Auth passam.