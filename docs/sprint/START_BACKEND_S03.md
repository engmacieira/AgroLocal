# 🚀 Por Onde Começar: Sprint 03 (Backend)

**Foco:** Segurança, Autenticação (JWT) e Persistência de Usuários.
**Meta:** Ao final, o endpoint `/login` deve retornar um token real e a rota `/users/me` deve buscar do banco.

---

## 🛠️ Passo 1: Preparar o Terreno (15 min)
1.  **Instale as dependências de criptografia:**
    ```bash
    pip install "passlib[bcrypt]" "python-jose[cryptography]" "python-multipart"
    pip freeze > requirements.txt
    ```
2.  **Crie a chave secreta:**
    * Rode `openssl rand -hex 32` no terminal.
    * Copie o código gerado.
    * Coloque no seu `.env`: `SECRET_KEY=seu_codigo_aqui`.

## 🔐 Passo 2: O Núcleo da Segurança (40 min)
Crie o arquivo `app/core/security.py`. Ele deve conter:
1.  `PwdContext` (passlib) para fazer hash de senhas.
2.  Função `verify_password(plain, hashed)`.
3.  Função `get_password_hash(password)`.
4.  Função `create_access_token(data, expires_delta)`.

## 👮 Passo 3: O "Porteiro" (Middlewares) (30 min)
Crie o arquivo `app/api/deps.py`.
1.  Crie a dependência `get_current_user`.
2.  Ela deve ler o header `Authorization: Bearer ...`.
3.  Decodificar o JWT.
4.  Buscar o usuário no Banco de Dados (`db.query(User)...`).
5.  Se falhar, lançar `HTTPException(status_code=401)`.

## 🚪 Passo 4: Rotas de Entrada (1h)
Crie o arquivo `app/routers/auth_router.py`.
1.  **POST /signup:**
    * Recebe `UserCreate`.
    * Verifica se email já existe.
    * Hasheia a senha (`security.get_password_hash`).
    * Salva no banco (User + ProducerProfile).
2.  **POST /login:**
    * Recebe `OAuth2PasswordRequestForm` (padrão FastAPI).
    * Busca user pelo email.
    * Verifica senha (`security.verify_password`).
    * Retorna `{ "access_token": "...", "token_type": "bearer" }`.

## 🧪 Passo 5: Teste Real
1.  Abra o Swagger (`/docs`).
2.  Crie um usuário no `/signup`.
3.  Tente logar no `/login` (clique no cadeado 🔓 no topo direito do Swagger).
4.  Se o cadeado fechar 🔒, você venceu!

---

**💡 Dica de Ouro:** Não mexa no `mock_router.py` ainda. Crie os arquivos novos. Quando o Auth estiver pronto, nós vamos aos poucos substituindo os Mocks pelas rotas reais.