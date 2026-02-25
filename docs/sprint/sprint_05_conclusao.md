# 🏁 Log de Sprint: 05 e 05.1 - Ofertas, Logística e Busca Inteligente

**Período:** 25/02/2026
**Status:** Concluído
**Foco:** Implementar a entidade `ProducerProduct` (Oferta/Prateleira), estabelecendo a ligação entre o Produtor e o Catálogo Global, adicionando precisão financeira, controlo de estoque e malha logística.

## 🚀 Entregas Realizadas (O Que)
* **[Domínio]** Criação das entidades `ProducerProduct`, `ProductImage` e `DeliveryOption`. Regras estritas aplicadas: preço > 0, estoque não-negativo, taxa de entrega não-negativa.
* **[Infra]** Modelos SQLAlchemy com uso obrigatório de `Numeric(10, 2)` para lidar com dinheiro sem falhas de ponto flutuante. Implementação de busca `ILIKE` para suporte a sinônimos no catálogo.
* **[Aplicação]** Casos de Uso cobrindo a criação da oferta, movimentação de estoque (add/sub), definição de opções de entrega (Domicílio, Feira, Retirada) e upload de imagens.
* **[Apresentação]** Schemas rigorosos garantindo validação matemática na entrada da API (`gt=0`, `ge=0`) e rotas completas (`/offers` e `/catalog/products/search`).
* **[Qualidade]** TDD garantindo a integridade de ponta a ponta. Correção de falsos positivos na persistência em cascata (`cascade="all, delete-orphan"`) e ajuste no serializador de Decimals do Pydantic.

## 🧠 Retrospectiva (O Como)
### ✅ O que funcionou bem?
* **Visão de Produto:** A pausa estratégica para analisar a "Jornada do Usuário" revelou a necessidade crítica de Opções de Entrega e Busca por Sinônimos antes de avançarmos para o Carrinho de Compras.
* O uso de `Decimal` desde o Domínio até ao Banco de Dados garantiu que o sistema está pronto para transações financeiras reais.

### ⚠️ Lições Aprendidas / Obstáculos
* **SQLAlchemy Cascade:** Relacionamentos de "Um-para-Muitos" exigem a configuração explícita de `cascade` no modelo para que listas filhas (como opções de entrega) sejam gravadas corretamente no método `merge()`.
* **Herança em Dublês:** A adição de um método num contrato de repositório (`abstractmethod`) quebra imediatamente todos os *Fake Repositories* que não o implementam.

---

## 📊 Status Final
* **Próximos Passos:** Iniciar a Sprint 06 focada no Carrinho de Compras e Pedidos (`Order` e `OrderItem`). Os clientes agora precisam colocar essas ofertas na sacola!

---
**Assinatura:** Mark Construtor & Matheus