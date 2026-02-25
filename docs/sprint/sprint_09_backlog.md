# ⭐ Sprint 09: Sistema de Avaliações e Reputação (Reviews)

**Objetivo:** Permitir que clientes avaliem pedidos recebidos (com nota, comentário e foto) para construir a reputação dos produtores locais.
**Status:** Planeamento
**Entidades Principais:** `Review` e atualização na `Order`.

---

## 🎯 Backlog de Funcionalidades

### 📝 1. Captura da Avaliação (O Feedback)
* **[US-01] Avaliação de Compra Verificada:** Um cliente só pode avaliar um pedido que lhe pertence e que esteja com o status `DELIVERED` ou `COMPLETED`.
* **[US-02] Regra de Ouro (1:1):** Cada pedido só pode receber exatamente uma (1) avaliação.
* **[US-03] Sistema de Notas e Mídia:** O cliente deve fornecer uma nota estrita de 1 a 5 estrelas. Pode opcionalmente enviar um comentário em texto e uma foto do produto recebido (`photo_url`).

### 📊 2. Reputação do Produtor
* **[US-04] Vitrine de Avaliações:** O frontend deve poder listar as avaliações de um produtor específico para exibir no seu perfil público.
* **[US-05] Limpeza de Dados:** Comentários compostos apenas por espaços vazios devem ser higienizados e convertidos para nulos.

---

## 💳 Regras de Negócio Core (Domínio)
* **Proteção de Intervalo:** O sistema não pode, sob nenhuma circunstância, aceitar notas `< 1` ou `> 5`.
* **Imutabilidade Base:** Uma vez submetida, a avaliação vincula-se permanentemente àquele `order_id`.

---

## 🛠️ Plano Técnico de Execução
1. **Domínio (RED/GREEN):** Criar entidade `Review` com validação de notas e higienização de texto.
2. **Infraestrutura:** Criar `ReviewModel` (com `CheckConstraint` no banco) e Repositório. Atualizar `OrderModel` para a relação 1:1.
3. **Aplicação:** Criar `CreateReviewUseCase` validando o status da `Order`.
4. **Apresentação:** Rotas para enviar a avaliação e para listar o feedback do produtor.