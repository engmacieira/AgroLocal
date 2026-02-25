# 🕵️ Sprint 11: Trilha de Auditoria e Compliance (Audit Log)

**Objetivo:** Implementar a "Caixa Preta" do sistema, registando de forma imutável quem fez o quê, quando e a partir de onde, armazenando o delta (o antes e o depois) das alterações críticas.
**Status:** Planeamento
**Entidades Principais:** `AuditLog` e `AuditAction`.

---

## 🎯 Backlog de Funcionalidades

### 🔍 1. O "Gravador de Voo" (Audit Log)
* **[US-01] Registo Universal:** O sistema deve ser capaz de registar ações (`CREATE`, `UPDATE`, `DELETE`, `LOGIN`, etc.) para qualquer tabela do sistema (`table_name` e `record_id`).
* **[US-02] O Delta das Mudanças:** Para ações de `UPDATE`, o sistema deve armazenar um snapshot JSON do `old_values` (antes da alteração) e `new_values` (depois da alteração).
* **[US-03] Contexto de Rastreabilidade:** Guardar o `actor_id` (quem fez), o `ip_address` e o `user_agent` (dispositivo/browser usado).

### 🛡️ 2. Regras de Compliance (Domínio)
* **[US-04] Imutabilidade Total:** Um registo de auditoria, uma vez criado, nunca pode ser editado nem apagado (Append-Only).
* **[US-05] Validação de Coerência:** Se a ação for `UPDATE`, tem de existir obrigatoriamente um payload em `old_values` e `new_values`. Se for `CREATE`, não deve haver `old_values`.

---

## 🛠️ Plano Técnico de Execução
1. **Domínio (RED/GREEN):** Criar a entidade `AuditLog` e as validações de coerência dos payloads JSON.
2. **Infraestrutura:** Ajustar o `AuditModel` (garantindo que `record_id` suporta UUIDs convertidos para string) e criar o repositório (`save` e `get_by_filters`).
3. **Aplicação/Apresentação:** (Opcional por agora) Criar um Caso de Uso interno para os outros serviços chamarem, ou um serviço de background que interceta eventos do SQLAlchemy. *Para o MVP Base, vamos focar em deixar a estrutura e a injeção prontas.*