# 🚜 Sprint 03: Perfil do Produtor (ProducerProfile)

**Objetivo:** Implementar a camada de negócio para o Vendedor, permitindo que usuários se tornem produtores aptos a comercializar produtos no marketplace.
**Status:** Planejamento
**Entidade:** `ProducerProfile`

---

## 🎯 Backlog de Funcionalidades

### 🏪 1. Perfil e Identidade Comercial
* **[US-01] Tornar-se Produtor (Create Profile)**
    * Vincular um `User` existente a um novo `ProducerProfile`.
    * Campos obrigatórios: Nome da Loja, CPF/CNPJ, Chave PIX.
* **[US-02] Gestão de Perfil (Read/Update)**
    * Editar Bio, Nome da Loja e Chave PIX.
    * Exibir métricas (Rating médio - inicializado em 0).
* **[US-03] Desativação de Vendedor (Soft Delete)**
    * Permitir que o produtor encerre suas atividades sem excluir o usuário base.

### 💳 2. Regras de Negócio (Domínio)
* **Validação de Documento:** Impedir CPFs/CNPJs em formato inválido.
* **Unicidade:** Um usuário só pode ter um (1) perfil de produtor ativo (Relação 1:1).

---

## 🛠️ Atributos da Entidade
| Atributo | Tipo | Descrição |
| :--- | :--- | :--- |
| `user_id` | UUID | FK para o Usuário (Dono do perfil) |
| `store_name`| String | Nome fantasia da lojinha |
| `document` | String | CPF ou CNPJ (apenas números) |
| `pix_key` | String | Chave para recebimento |
| `bio` | String | Descrição dos produtos/história |
| `rating` | Float | Média de avaliações (0.0 a 5.0) |

---

## 📝 Definição de Pronto (DoD)
* [ ] Entidade rica criada e testada.
* [ ] Repositório implementado e persistindo no banco.
* [ ] Casos de uso orquestrando a criação e edição.
* [ ] Endpoints FastAPI funcionando com validação Pydantic.