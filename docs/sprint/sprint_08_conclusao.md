# 🏁 Log de Sprint: 08 - Repasses Financeiros (Outflow) e Fechamento

**Período:** 25/02/2026
**Status:** Concluído
**Foco:** Implementar o motor de Repasses (`Payout`), calcular a comissão da plataforma, gerir o status de conclusão do pedido e simular o envio de dinheiro para o produtor.

## 🚀 Entregas Realizadas (O Que)
* **[Domínio]** Criação da entidade `Payout` com regras estritas de matemática financeira (Gross, Fee, Net) e imutabilidade de chave PIX (Snapshot). Atualização da máquina de estados de `Order` com o novo status final `COMPLETED`.
* **[Infra]** Implementação do `PayoutModel` com relação 1:1 com `Order`. Persistência segura garantindo que o valor líquido é sempre gravado corretamente no banco.
* **[Aplicação]** Casos de Uso inteligentes: `SchedulePayoutUseCase` (calcula e agenda os 10% de taxa da plataforma) e `ProcessPayoutUseCase` (confirma o recibo bancário e avança a Ordem original para `COMPLETED` em cascata).
* **[Apresentação]** Schemas e endpoints focados na operação do Administrador (`/payouts/schedule`, `/payouts/{id}/process`, etc.).
* **[Qualidade]** Cobertura E2E completa validando a jornada financeira do Administrador: desde o agendamento após a entrega, passando pela matemática exata da plataforma, até à conclusão definitiva do pedido.

## 🧠 Retrospectiva (O Como)
### ✅ O que funcionou bem?
* **Separação Inflow/Outflow:** Tratar a entrada de dinheiro (`Transaction` - Sprint 07) em separado da saída de dinheiro (`Payout` - Sprint 08) evitou o acoplamento excessivo e permitiu que a taxa da plataforma fosse calculada num momento mais oportuno e seguro.
* **Cascata Lógica (Domain Events simulado):** A forma como o `ProcessPayoutUseCase` atualiza o Payout e em seguida muda a Ordem para `COMPLETED` encapsula perfeitamente a regra de negócio num único fluxo transacional.

### ⚠️ Lições Aprendidas / Obstáculos
* **Atenção aos Relacionamentos 1:1:** O uso do `uselist=False` no SQLAlchemy foi fundamental para garantir que um Pedido só pode ter um único Repasse, protegendo a plataforma de pagar duas vezes a mesma venda.

---

## 📊 Status Final
* **Próximos Passos:** Iniciar a Sprint 09 focada exclusivamente no Sistema de Avaliações (`Review`). Permitir que o cliente dê uma nota (1 a 5 estrelas) ao produtor após o pedido ser entregue.

---
**Assinatura:** Mark Construtor & Matheus