# 📦 Sprint 05: Gestão de Ofertas (A Prateleira do Produtor)

**Objetivo:** Permitir que produtores vinculem seus perfis a produtos do Catálogo Global, definindo preço, estoque, unidade de medida e fotos reais da colheita.
**Status:** Planejamento
**Entidades Principais:** `ProducerProduct` e `ProductImage`

---

## 🎯 Backlog de Funcionalidades

### 🏪 1. Criação e Gestão de Ofertas
* **[US-01] Criar Oferta:** O produtor escolhe um item do catálogo (ex: Tomate Carmem) e define o Preço (R$), Unidade (kg, maço) e Estoque inicial.
* **[US-02] Atualizar Oferta:** Modificar o preço, a descrição ou a data da colheita (`harvest_date`).
* **[US-03] Movimentação de Estoque:** Adicionar ou remover unidades do estoque atual.
* **[US-04] Pausar Vendas (Soft Delete):** Desativar a oferta sem perder o histórico (`is_active = False`).

### 📸 2. Galeria da Oferta
* **[US-05] Adicionar Fotos Reais:** Anexar imagens (`ProductImage`) à oferta para mostrar a qualidade real da colheita ao cliente.

---

## 💳 Regras de Negócio (Domínio)
* **Preço Justo:** O valor da oferta (`price`) deve ser estritamente maior que zero.
* **Estoque Real:** A quantidade em estoque (`stock_quantity`) não pode ficar negativa.
* **Venda Mínima:** A quantidade mínima de pedido (`minimum_order_quantity`) deve ser maior que zero.

---

## 🛠️ Plano Técnico de Execução (Baby Steps / TDD)
1. **Domínio (RED/GREEN):** Testes e Entidade `ProducerProduct` (com validações de preço e estoque).
2. **Infraestrutura:** Modelo SQLAlchemy `product_model.py` (usando Numeric/Decimal) e o `OfferRepository`.
3. **Aplicação:** Casos de uso (`CreateOffer`, `UpdateStock`, etc.).
4. **Apresentação:** Endpoints do Produtor (`/offers`).