# 💬 Sprint 10: Comunicação, Chamados e Auditoria (Messaging)

**Objetivo:** Implementar um sistema estruturado de conversas (Tickets/Chats) com foco em auditoria, histórico e regras de comunicação estritas entre os diferentes atores da plataforma (Cliente, Produtor e Admin).
**Status:** Planeamento
**Entidades Principais:** `Conversation` (O Chamado/Tópico) e `Message` (A Mensagem individual).

---

## 🎯 Backlog de Funcionalidades

### 🗂️ 1. O Tópico da Conversa (Conversation)
* **[US-01] Criação com Contexto:** Um utilizador pode abrir uma conversa especificando o Assunto (`SubjectType`).
* **[US-02] Vinculação de Entidades:** A conversa deve permitir guardar um `reference_id` opcional (ex: o ID da Ordem de Compra ou o ID do Produto) para facilitar o atendimento.
* **[US-03] Ciclo de Vida do Chamado:** Uma conversa tem um `status` (OPEN, RESOLVED, CLOSED).

### 💬 2. O Histórico de Mensagens (Message)
* **[US-04] Rastreabilidade de Papéis:** Cada mensagem regista explicitamente o `sender_role` (CUSTOMER, PRODUCER, ADMIN) para facilitar a leitura e filtragem.
* **[US-05] Timestamp e Auditoria:** Cada mensagem é imutável e regista a data e hora exatas do envio.

---

## 💳 Regras de Negócio Core (Domínio)
* **Isolamento de Papéis:** Clientes NÃO podem conversar com outros Clientes.
* **Comunicação Direta:** Numa conversa sobre um Pedido (`ORDER_ISSUE`), os únicos papéis permitidos são o Cliente que comprou, o Produtor que vendeu e o Admin (em caso de mediação).
* **Imutabilidade:** Uma mensagem não pode ser editada ou apagada após o envio (Regra de Auditoria).
* **Bloqueio de Conversa Fechada:** Não se pode adicionar novas mensagens a uma `Conversation` que já esteja `CLOSED`.

---

## 🛠️ Plano Técnico de Execução
1. **Domínio (RED/GREEN):** Criar `Conversation` e `Message` com os Enums de assunto e regras de bloqueio.
2. **Infraestrutura:** Criar `ConversationModel` e `MessageModel` (Relação 1:N) e repositórios correspondentes.
3. **Aplicação:** `StartConversationUseCase` e `SendMessageUseCase`.
4. **Apresentação:** Rotas para listar conversas de um utilizador e enviar novas mensagens.