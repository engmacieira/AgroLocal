# 📱 Por Onde Começar: Sprint 03 (Frontend)

**Foco:** Criação das telas de Login, Cadastro e Vitrine consumindo a API Mock.
**Meta:** Ter um App navegável onde o usuário "loga" e vê produtos.

---

## 🔌 Passo 0: Conectar na API (Importante!)
Como o Backend está rodando na máquina do Matheus (ou localmente), você precisa apontar o Axios para o lugar certo.
1.  **Se estiver no Emulador Android:** Use `http://10.0.2.2:8000`.
2.  **Se estiver no iPhone/Físico:** Use o IP da rede local (Ex: `http://192.168.1.XX:8000`).
3.  **Teste:** Abra o navegador do celular e digite `http://[IP]:8000/docs`. Se carregar o Swagger, a conexão está OK.

## 🧱 Passo 1: Estrutura de Navegação (1h)
Configure o **React Navigation**:
1.  **AuthStack:** Telas `LoginScreen` e `SignUpScreen`.
2.  **AppStack:** Tab Navigator (`HomeScreen`, `OrdersScreen`, `ProfileScreen`).
3.  **Lógica:** Se tiver token salvo, mostra `AppStack`. Se não, `AuthStack`.

## 👤 Passo 2: Tela de Login (Mock) (1h)
1.  Crie um formulário (Email/Senha).
2.  No submit, faça um POST para `/mocks/auth/login`.
    * *Nota:* Pode enviar qualquer senha, o mock sempre aceita.
3.  Receba o token e salve (AsyncStorage/SecureStore).
4.  Redirecione para a Home.

## 🍎 Passo 3: Vitrine de Produtos (Home) (1.5h)
1.  Faça um GET em `/mocks/categories` para montar o carrossel do topo.
2.  Faça um GET em `/mocks/products/offers` para listar os cards.
3.  **Exibição:**
    * Use o campo `images[0].url` para a foto.
    * Use `global_info.name` para o título.
    * Use `price` e `unit` para o preço (Ex: "R$ 8,50 / kg").

## 🛒 Passo 4: Fluxo de Compra (Checkout) (1.5h)
1.  Ao clicar "Comprar", monte o JSON conforme o Schema `OrderCreate` (veja no Swagger).
2.  Faça POST em `/mocks/orders`.
3.  Pegue o ID do pedido retornado.
4.  Faça POST em `/mocks/transactions` enviando `payment_method: "PIX"`.
5.  **O Grand Finale:** Exiba o QR Code que vem no campo `pix_qr_code_base64`.

---

**💡 Dica:** Todos os dados que você precisa (JSONs de exemplo) estão visíveis em `http://localhost:8000/docs`. Use o Swagger como sua "Bíblia" de tipos e campos.