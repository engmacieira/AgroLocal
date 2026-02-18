# 🏁 Log de Sprint: 01 - Fundação e Modelagem Profissional

**Período:** 18/02/2026
**Status:** Concluído
**Foco:** Infraestrutura base, configuração de ambiente Docker e modelagem de dados com UUID.

## 🚀 Entregas Realizadas (O Que)
* **[Infra]** Configuração do `docker-compose.yaml` com PostgreSQL 15 na porta 5434.
* **[Infra]** Setup do Alembic com suporte a tipos customizados (`GUID`).
* **[Backend]** Modelagem completa de Usuários, Perfis, Produtos (Global e Produtor), Pedidos, Financeiro e Auditoria.
* **[Arquitetura]** Implementação de UUIDs v4 como chaves primárias em todas as tabelas para maior segurança e escalabilidade.

## 🧠 Retrospectiva (O Como)
### ✅ O que funcionou bem?
* A decisão de pular o SQLite e ir direto para o Postgres poupou retrabalho de migração futuro.
* O uso de Enums para status de pedidos e produtos garante que as regras de negócio sejam respeitadas desde o banco de dados.

### ⚠️ Lições Aprendidas / Obstáculos
* O Alembic não importa automaticamente módulos customizados nos scripts gerados. Tivemos que adicionar o `import app.core.database` manualmente no arquivo de versão.

---

## 📊 Status Final
* **Dívidas Técnicas Geradas:** Nenhuma crítica.
* **Próximos Passos:** Iniciar o Módulo de Autenticação (SignUp/SignIn) e as primeiras rotas de API.