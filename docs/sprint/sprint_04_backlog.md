# 🛒 Sprint 04: Catálogo Global (Taxonomia e Curadoria)

**Objetivo:** Implementar o dicionário mestre de produtos e categorias do AgroLocal, garantindo que não haja duplicidade de itens na plataforma.
**Status:** Planejamento
**Entidades Principais:** `Category` e `GlobalProduct`

---

## 🎯 Backlog de Funcionalidades

### 🗂️ 1. Gestão de Categorias
* **[US-01] Criar Categoria:** Cadastrar categorias base (ex: "Frutas", "Legumes", "Laticínios") com geração automática de *slug* para URLs amigáveis.
* **[US-02] Listar Categorias:** Retornar as categorias ativas para exibição no App.

### 📖 2. Catálogo de Produtos Globais (A "Verdade")
* **[US-03] Sugerir Produto Global:** Permitir a criação de um novo item no catálogo mestre (Nome, Sinônimos, Categoria, NCM).
* **[US-04] Curadoria de Catálogo:** Alterar o status do produto (PENDING, APPROVED, REJECTED, ARCHIVED) com registro de quem revisou e motivo da rejeição.
* **[US-05] Busca no Catálogo:** Listar produtos globais aprovados para que os produtores possam escolhê-los futuramente.

---

## 💳 Regras de Negócio (Domínio)
* **Status Inicial:** Todo produto global nasce como `PENDING` (Aguardando Análise), a menos que seja criado diretamente por um Admin.
* **Rejeição:** Um produto global só pode ir para o status `REJECTED` se for fornecido um motivo de rejeição (`rejection_reason`).
* **Slugs Únicos:** O nome da categoria deve gerar um identificador amigável (Ex: "Frutas Cítricas" vira "frutas-citricas").

---

## 🛠️ Plano Técnico de Execução (Baby Steps / TDD)
1. **Domínio (RED/GREEN):** Testes e Entidades para `Category` e `GlobalProduct`.
2. **Infraestrutura:** Modelos SQLAlchemy refletindo o `catalog_model.py` e repositórios reais.
3. **Aplicação:** Casos de Uso em `catalog_management.py`.
4. **Apresentação:** Schemas e Router em `/catalog`.