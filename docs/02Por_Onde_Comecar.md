# 🤖 Contexto de Continuidade: AgroLocal

> **PARA O AGENTE/DESENVOLVEDOR (MARK):**
> Este arquivo é o seu Ponto de Restauração. Antes de processar qualquer novo prompt, analise este estado para garantir consistência com a sessão anterior.

## 📍 Estado Atual da Missão
* **Fase do Projeto:** Fim do Core Transacional (MVP Backend Base Concluído).
* **Sprints Concluídas:** Sprints 01 a 09.
* **Última Ação Realizada:** Finalizamos 100% da Sprint 09. O sistema de Avaliações (`Review`) está implementado com sucesso.
* **Estado da Aplicação:** O AgroLocal possui autenticação, gestão de perfis, catálogo global mestre, vitrines de produtores, carrinho inteligente (split), pagamentos unificados, repasses com taxa de plataforma, máquina de estados do pedido e sistema de reputação 1 a 5 estrelas. Tudo coberto por testes.
* **PRÓXIMO PASSO IMEDIATO:** Definir o rumo do projeto. As opções são: iniciar a Sprint 10 (Notificações/Websockets para chat), preparar o deploy da API (Docker/AWS) ou focar no desenvolvimento do Frontend/Mobile.

## 🏗️ Definições Arquiteturais (Não Quebrar)
* **Backend:** Python (FastAPI) + SQLAlchemy + DDD estrito.
* **Dinheiro:** Sempre usar `Decimal` para valores.
* **Testes:** TDD é obrigatório (Red-Green-Refactor).

## 🧭 Mapa da Verdade (Onde buscar detalhes)
* **Logs anteriores:** Consulte os arquivos na pasta `docs/sprint/`.

---
*Atualizado em: 25/02/2026*