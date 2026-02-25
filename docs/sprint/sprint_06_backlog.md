# 🛍️ Sprint 06: Carrinho Inteligente e Gestão de Pedidos (Orders)

**Objetivo:** Implementar a jornada de compra do cliente, com busca global, divisão de carrinho por produtor, cálculo inteligente de frete e máquina de estados do pedido.
**Status:** Planejamento
**Entidades Principais:** `Order`, `OrderItem` e `CartProcessor` (Serviço de Domínio/Aplicação).

---

## 🎯 Backlog de Funcionalidades

### 🔍 1. Busca Omnichannel para o Cliente
* **[US-01] Buscar Ofertas:** Permitir ao cliente buscar ofertas ativas por categoria, por produtor ou por texto (nome/sinônimo do produto global).

### 🛒 2. O Carrinho Inteligente (Checkout)
* **[US-02] Split de Pedidos:** Receber um carrinho misto e dividir em `N` Pedidos (`Orders`), um para cada Produtor.
* **[US-03] Lógica de Frete:** O frete de um pedido não é a soma dos fretes dos itens, mas sim o **maior valor** de frete entre os itens escolhidos para aquela modalidade de entrega.
* **[US-04] Reserva de Estoque:** Ao gerar o pedido (Status `CREATED`), o estoque do produtor é imediatamente deduzido para evitar *overbooking*.

### 📦 3. Máquina de Estados (Workflow do Pedido)
* **[US-05] Pagamento:** Transição de `CREATED` para `PAID` (O aceite do produtor agora é automático).
* **[US-06] Preparação e Entrega:** Transições lineares: `PAID` -> `PREPARING` -> `READY` (Pronto para retirada/envio) -> `DELIVERED`.
* **[US-07] Cancelamento e Estorno:** Transição para `CANCELED`. Exige preenchimento obrigatório de justificativa.

---

## 💳 Regras de Negócio Core (Domínio)
* **Snapshot Fiscal:** O `OrderItem` deve ser imutável após criado. Ele tira uma "foto" do nome do produto, unidade e preço no momento do clique.
* **Estado Inválido:** Um pedido não pode pular de `CREATED` direto para `DELIVERED`. A máquina de estados deve ser respeitada.

---

## 🛠️ Plano Técnico de Execução
1. **Domínio (RED/GREEN):** Entidades `Order`, `OrderItem` e testes focados no cálculo de totais, frete máximo e transições de status.
2. **Infraestrutura:** Modelo SQLAlchemy baseado no `order_model.py` (com `Numeric` e Snapshots).
3. **Aplicação:** Caso de Uso `CheckoutCart` (O grande orquestrador que faz o Split e a reserva de estoque).
4. **Apresentação:** Endpoints `/orders` para clientes (comprar) e para produtores (gerenciar status).