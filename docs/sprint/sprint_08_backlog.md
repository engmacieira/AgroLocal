# 💸 Sprint 08: Repasses Financeiros (Payouts) e Fechamento de Pedidos

**Objetivo:** Implementar o motor de Outflow, calculando a comissão da plataforma, agendando o repasse ao produtor após a entrega e marcando o pedido como definitivamente concluído.
**Status:** Planejamento
**Entidades Principais:** `Payout` e atualização na `Order`.

---

## 🎯 Backlog de Funcionalidades

### 🏦 1. O Motor de Repasse (Payout)
* **[US-01] Snapshots Bancários:** Salvar a chave PIX do produtor no momento do repasse para proteger o histórico caso ele mude de conta no futuro.
* **[US-02] Matemática Financeira:** Garantir que o `amount_net` (líquido do produtor) é estritamente igual a `amount_gross` (total da venda) menos `amount_fee` (taxa da plataforma).
* **[US-03] Agendamento:** Quando o pedido é marcado como `DELIVERED`, o sistema deve gerar automaticamente um `Payout` com status `SCHEDULED` e uma data prevista (`scheduled_for`).

### 🔄 2. O Fechamento do Pedido (Admin)
* **[US-04] Execução do Repasse:** O Admin anexa o comprovante (`proof_url` ou `bank_transaction_id`) e muda o Payout para `PAID`, registrando a data de processamento (`processed_at`).
* **[US-05] Status de Conclusão:** Ao confirmar o Payout, a `Order` original deve avançar de `DELIVERED` para `COMPLETED`.
* **[US-06] Tratamento de Falhas:** Permitir que o Admin marque o repasse como `FAILED` (ex: chave PIX rejeitada), exigindo um motivo (`failure_reason`).

---

## 💳 Regras de Negócio Core (Domínio)
* **Prevenção de Fraude:** Não se pode gerar um `Payout` se a Ordem não estiver, no mínimo, como `DELIVERED`.
* **Matemática Exata:** A taxa não pode ser maior que o valor bruto. O valor líquido não pode ser negativo.
* **Comprovação:** Um Payout não pode virar `PAID` sem que haja um comprovante de transação bancária.

---

## 🛠️ Plano Técnico de Execução
1. **Domínio (RED/GREEN):** Atualizar `OrderStatus`, criar `Payout` e garantir a matemática financeira.
2. **Infraestrutura:** Criar `PayoutModel` e Repositório.
3. **Aplicação:** Criar Caso de Uso `ProcessPayoutUseCase` (Admin confirma a transferência e finaliza a Ordem).
4. **Apresentação:** Rotas para o painel de Administração listar Payouts pendentes e confirmar repasses.