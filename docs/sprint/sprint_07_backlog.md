# 💳 Sprint 07: Pagamento Unificado e Transações (Gateway)

**Objetivo:** Permitir que o cliente faça um pagamento único para múltiplos pedidos gerados num mesmo checkout, e processar o retorno de sucesso/falha simulando um Gateway de Pagamentos.
**Status:** Planejamento
**Entidades Principais:** `Transaction` e `Order` (atualizada).

---

## 🎯 Backlog de Funcionalidades

### 💰 1. Pagamento Unificado (O PIX do Carrinho)
* **[US-01] Gerar Transação Única:** Agrupar uma lista de pedidos (`Orders`) recém-criados numa única `Transaction`.
* **[US-02] Cálculo do Total do Gateway:** O valor da `Transaction` (`amount`) deve ser a soma exata do `total_amount` de todos os pedidos atrelados.
* **[US-03] Dados de Cobrança:** Gerar dados simulados de PIX (QR Code e Copia-e-Cola) para exibir ao cliente.

### 🔄 2. O Webhook de Confirmação (Máquina de Estados)
* **[US-04] Processar Pagamento Aprovado:** Criar um endpoint para receber o "Aviso de Pagamento" (simulando um Webhook do Stripe/MercadoPago).
* **[US-05] Atualização em Lote (Cascade):** Quando a `Transaction` muda para `APPROVED`, todos os pedidos vinculados mudam automaticamente para `PAID`.
* **[US-06] Processar Falhas:** Se o pagamento falhar ou expirar (`FAILED` / `EXPIRED`), liberar o estoque que estava reservado nos produtos.

---

## 💳 Regras de Negócio Core (Domínio)
* **Transação Imutável:** O valor (`amount`) da transação é bloqueado após a criação.
* **Tudo ou Nada:** Se a transação é aprovada, TODOS os pedidos daquela transação são marcados como pagos.
* **Proteção de Estoque:** Transações expiradas devem devolver a quantidade de volta ao `ProducerProduct`.

---

## 🛠️ Plano Técnico de Execução
1. **Ajuste de Banco (Infra):** Mover a FK de pagamento. Remover `order_id` de `Transaction` e adicionar `transaction_id` no modelo `Order`.
2. **Domínio (RED/GREEN):** Entidade `Transaction` capaz de receber uma lista de `Orders` e somar os totais.
3. **Aplicação:** Casos de uso `GeneratePaymentUseCase` e `ProcessWebhookUseCase`.
4. **Apresentação:** Rotas `/transactions` para gerar o PIX e receber o status pago.