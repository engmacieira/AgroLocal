# 🏁 Log de Sprint: 04 - Catálogo Global e Categorias

**Período:** 24/02/2026
**Status:** Concluído
**Foco:** Implementar o dicionário mestre de produtos (`GlobalProduct`) e a taxonomia do sistema (`Category`), garantindo a padronização antes de permitir vendas.

## 🚀 Entregas Realizadas (O Que)
* **[Domínio]** Criação das entidades `Category` (com suporte a ícones) e `GlobalProduct` (com workflow de moderação: PENDING, APPROVED, REJECTED).
* **[Infra]** Modelos e Repositórios SQLAlchemy implementados, garantindo a unicidade de nomes de categorias e produtos.
* **[Aplicação]** Casos de Uso cobrindo a geração automática de `slugs` para URLs amigáveis e a orquestração da moderação (aprovação/rejeição com exigência de motivo).
* **[Apresentação]** Schemas Pydantic e endpoints FastAPI (`/catalog`) para sugerir produtos, listar por status (Admin) e listar por categoria (Produtores).
* **[Qualidade]** 100% de cobertura nos fluxos com TDD (Domain, Infra, App e Presentation), validando desde a rejeição sem motivo até a listagem de vitrines aprovadas.

## 🧠 Retrospectiva (O Como)
### ✅ O que funcionou bem?
* **Princípio da Responsabilidade Única (SRP):** Separar o conceito de "O que é o produto" (Catálogo Global) de "Quem está vendendo e por quanto" (Oferta do Produtor) blindou o sistema contra dados sujos.
* **Inteligência na Aplicação:** A lógica de higienização de strings para gerar os `slugs` dentro do Caso de Uso evitou que o frontend precisasse tratar isso.

### ⚠️ Lições Aprendidas / Obstáculos
* Nenhum grande bloqueio. O domínio prévio das camadas acelerou imensamente a entrega das rotas auxiliares no final da Sprint.

---

## 📊 Status Final
* **Próximos Passos:** Iniciar a Sprint 05 focada na Entidade `ProducerProduct` (A Oferta). Agora que temos as prateleiras e os rótulos, vamos colocar os preços e o estoque!

---
**Assinatura:** Mark Construtor & Matheus