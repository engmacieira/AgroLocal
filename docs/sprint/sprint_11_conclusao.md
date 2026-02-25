# 🏁 Log de Sprint: 11 - Trilha de Auditoria e Compliance (Audit Log)

**Período:** 25/02/2026
**Status:** Concluído
**Foco:** Implementar a "Caixa Preta" do sistema (Audit Log), capaz de rastrear alterações críticas em qualquer tabela, guardando de forma imutável quem alterou, o que foi alterado (Deltas em JSON) e de onde (IP/User Agent).

## 🚀 Entregas Realizadas (O Que)
* **[Domínio]** Criação da entidade `AuditLog` com validações de coerência (ex: exigir `old_values` e `new_values` obrigatórios em ações de `UPDATE`) e higienização de IPs.
* **[Infra]** Implementação do `AuditModel` utilizando colunas do tipo `JSON` para armazenar o delta das alterações de forma agnóstica a tabelas. O repositório foi desenhado para ser estritamente *Append-Only* (somente inserção, nunca atualização ou exclusão).
* **[Aplicação]** Casos de Uso de gravação (`LogAuditActionUseCase`), que servirá de motor interno para o resto do sistema, e de leitura (`GetRecordAuditHistoryUseCase`).
* **[Apresentação]** Rota administrativa de leitura (`GET /audit/{table_name}/{record_id}`) para visualizar a linha do tempo de um registo específico.
* **[Qualidade]** Cobertura E2E garantindo que o histórico é salvo corretamente pelo repositório e devolvido com sucesso pela API.

## 🧠 Retrospectiva (O Como)
### ✅ O que funcionou bem?
* **O Poder do JSON:** Usar colunas JSON no SQLAlchemy permitiu criar um único modelo de Auditoria capaz de rastrear qualquer tabela do sistema (Produtos, Pedidos, Utilizadores), evitando a criação de dezenas de tabelas de histórico isoladas.
* **Design Interno vs Externo:** A decisão de não expor um endpoint `POST` público para criar logs protegeu a integridade do sistema, mantendo a gravação da auditoria como um processo estritamente interno e controlado pela camada de Aplicação.

---

## 📊 Status Final
* **Marco Alcançado:** O MVP do AgroLocal agora possui os pilares completos de transação, comunicação e **compliance/auditoria**.

---
**Assinatura:** Mark Construtor & Matheus