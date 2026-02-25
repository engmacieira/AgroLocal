# 🏁 Log de Sprint: 09 - Sistema de Avaliações e Reputação (Reviews)

**Período:** 25/02/2026
**Status:** Concluído
**Foco:** Implementar o sistema de "Prova Social" (Reviews), permitindo que os clientes avaliem os pedidos recebidos, com notas de 1 a 5, comentários e fotos reais dos produtos.

## 🚀 Entregas Realizadas (O Que)
* **[Domínio]** Criação da entidade `Review` com validação estrita (nota entre 1 e 5) e higienização automática de comentários vazios ou preenchidos apenas com espaços.
* **[Infra]** Implementação do `ReviewModel` atrelado 1:1 com a Ordem de Compra (`OrderModel`). Adição de uma `CheckConstraint` no banco de dados como última linha de defesa contra notas inválidas.
* **[Aplicação]** Criação do `CreateReviewUseCase`, que atua como "Guarda-Costas", garantindo que: 1) o pedido existe; 2) pertence a quem está a avaliar; 3) já foi entregue (`DELIVERED`/`COMPLETED`); 4) ainda não foi avaliado.
* **[Apresentação]** Schemas com validação Pydantic (`ge=1`, `le=5`) e rotas para envio de feedback (`POST /reviews/`) e exibição da vitrine do produtor (`GET /reviews/producer/{id}`).
* **[Qualidade]** Cobertura E2E garantindo que o sistema bloqueia avaliações prematuras e regista com sucesso a jornada completa após a entrega.

## 🧠 Retrospectiva (O Como)
### ✅ O que funcionou bem?
* **Fail-Fast com Pydantic e CheckConstraint:** Ao aplicar os limites de 1 a 5 no Pydantic (entrada) e no CheckConstraint do SQLAlchemy (banco), garantimos que o Domínio nunca seja poluído com lixo, aumentando a resiliência do sistema.
* **Proteção da Prova Social:** A regra estrita de que "só se avalia o que já foi recebido" (status DELIVERED) e a relação 1:1 protegem o produtor contra spam e avaliações falsas (Fake Reviews).

---

## 📊 Status Final
* **Marco Alcançado:** O fluxo transacional (Core E-commerce) do AgroLocal está 100% finalizado (Catálogo -> Carrinho -> Pagamento -> Repasse -> Avaliação).

---
**Assinatura:** Mark Construtor & Matheus