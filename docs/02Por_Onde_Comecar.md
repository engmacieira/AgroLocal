# 🤖 Contexto de Continuidade: AgroLocal

> **PARA O AGENTE/DESENVOLVEDOR (MARK):**
> Este arquivo é o seu Ponto de Restauração. Antes de processar qualquer novo prompt, analise este estado para garantir consistência com a sessão anterior.

## 📍 Estado Atual da Missão
* **Fase do Projeto:** Desenvolvimento (Sprint 06).
* **Sprint Atual:** Sprint 06 - Carrinho de Compras e Pedidos (`Order`).
* **Última Ação Realizada:** Finalizamos 100% da Sprint 05 (Ofertas e Logística). A plataforma agora tem uma busca inteligente por sinônimos e o produtor consegue definir preços (Decimal), estoque, fotos reais e opções de entrega (Domicílio, Retirada, Feira).
* **PRÓXIMO PASSO IMEDIATO:** Planejar o backlog da Sprint 06. Modelar o Domínio do Pedido (`Order`), que deve relacionar o Cliente (`User`) aos itens comprados (`OrderItem`), calcular o total financeiro somado ao frete selecionado, e gerir o status do pedido (Pendente, Confirmado, Em Rota, Entregue, Cancelado).

## 🏗️ Definições Arquiteturais (Não Quebrar)
* **Backend:** Python (FastAPI) + SQLAlchemy + DDD estrito.
* **Dinheiro:** Sempre usar `Decimal` para preços, taxas e totais.
* **Testes:** TDD é obrigatório (Red-Green-Refactor).

## 🧭 Mapa da Verdade (Onde buscar detalhes)
* **Logs anteriores:** Consulte os arquivos concluídos na pasta `docs/sprint/`.

---
*Atualizado em: 25/02/2026*