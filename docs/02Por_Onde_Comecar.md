# 🤖 Contexto de Continuidade: AgroLocal

> **PARA O AGENTE/DESENVOLVEDOR (MARK):**
> Este arquivo é o seu Ponto de Restauração. Antes de processar qualquer novo prompt, analise este estado para garantir consistência com a sessão anterior.

## 📍 Estado Atual da Missão
* **Fase do Projeto:** Fim do Core Transacional e Operacional (Backend Base Concluído).
* **Sprints Concluídas:** Sprints 01 a 10.
* **Última Ação Realizada:** Finalizamos 100% da Sprint 10. O sistema de Comunicação e Chamados (Ticketing) foi implementado com sucesso.
* **Estado da Aplicação:** O AgroLocal possui autenticação, gestão de perfis, catálogo, vitrines, carrinho inteligente (split), pagamentos unificados, repasses, máquina de estados do pedido, avaliações e agora **um sistema auditável de troca de mensagens e chamados**. Tudo coberto por testes.
* **PRÓXIMO PASSO IMEDIATO:** Definir o rumo do projeto pós-MVP Base. As opções são: preparar o ambiente de produção (Docker, CI/CD, Nuvem), iniciar desenvolvimento Frontend/Mobile, ou construir o Painel Administrativo de Analytics (Dashboards e Relatórios).

## 🏗️ Definições Arquiteturais (Não Quebrar)
* **Backend:** Python (FastAPI) + SQLAlchemy + DDD estrito.
* **Dinheiro:** Sempre usar `Decimal` para valores.
* **Testes:** TDD é obrigatório (Red-Green-Refactor).

## 🧭 Mapa da Verdade (Onde buscar detalhes)
* **Logs anteriores:** Consulte os arquivos na pasta `docs/sprint/`.

---
*Atualizado em: 25/02/2026*