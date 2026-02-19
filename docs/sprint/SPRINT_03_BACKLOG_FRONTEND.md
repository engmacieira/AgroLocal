# 📱 Sprint 03: Frontend - Layout e Integração (Mock First)

**Objetivo:** Construir a interface visual do aplicativo (Telas e Navegação) consumindo a API Mockada. O foco é UX/UI e fluxo de navegação, sem bloquear o desenvolvimento do Backend.
**Responsável:** Frontend Dev
**Status:** A Fazer
**Base URL:** `http://localhost:8000` (ou IP da sua máquina)

---

## 🧭 1. Navegação e Estrutura
* **[UI-00] Setup de Navegação**
    * **Tech:** React Navigation (Stack + Tab Navigator).
    * **Estrutura:**
        * **AuthStack:** Login, Cadastro.
        * **AppTabs:** Home (Vitrine), Busca, Carrinho, Pedidos, Perfil.

## 🔐 2. Telas de Acesso (Auth)
* **[UI-01] Tela de Login**
    * **Endpoint:** `POST /mocks/auth/login` (Simulado)
    * **Ação:** Salvar o token recebido no armazenamento local (AsyncStorage/SecureStore).
    * **Redirecionamento:** Ao logar, ir para a Home.

* **[UI-02] Tela de Cadastro**
    * **Schema:** `UserCreate` (Ver Swagger: `/docs`)
    * **Campos:** Nome, Email, Senha, Telefone.
    * **Switch:** "Quero vender produtos" (Se ativado, mostrar campos de Produtor: CPF, Nome da Loja).

## 🛒 3. Fluxo de Compra (Vitrine)
* **[UI-03] Home / Carrossel de Categorias**
    * **Endpoint:** `GET /mocks/categories`
    * **Exibição:** Lista horizontal com Ícone e Nome.

* **[UI-04] Listagem de Ofertas (Feed)**
    * **Endpoint:** `GET /mocks/products/offers`
    * **Exibição:** Card com Foto (`images[0].url`), Nome (`global_info.name`), Preço (`price`) e Unidade (`unit`).
    * **Mock Data:** Vai retornar Tomate e Queijo para teste.

* **[UI-05] Detalhe do Produto**
    * **Ação:** Ao clicar no Card, abrir modal/tela com descrição completa (`description`) e botão "Adicionar ao Carrinho".

## 👤 4. Área Logada
* **[UI-06] Tela de Perfil**
    * **Endpoint:** `GET /mocks/users/me`
    * **Exibição:** Avatar, Nome, E-mail.
    * **Condicional:** Se `role == "PRODUTOR"`, exibir card com "Minha Loja" e nota (`producer_profile.rating`).

---

## 📝 Definição de Pronto (DoD Frontend)
* [ ] Navegação fluida entre telas (Login -> Home -> Detalhe).
* [ ] Formulários validam campos básicos (email tem @, senha > 8 chars).
* [ ] O App não quebra se a API retornar erro (Tratamento de exceção básico).
* [ ] Layout fiel aos wireframes/mockups (se houver).