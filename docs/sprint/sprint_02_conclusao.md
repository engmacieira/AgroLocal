# 🏁 Log de Sprint: 02 - Gestão de Endereços (Address)

**Período:** 24/02/2026
**Status:** Concluído
**Foco:** Implementar a entidade `Address` com foco em logística rural e urbana, garantindo vínculo com o `User`.

## 🚀 Entregas Realizadas (O Que)
* **[Domínio]** Criação da entidade `Address` com suporte a `AddressType` (RESIDENCIAL, COMERCIAL, RURAL, PONTO_ENCONTRO) e geolocalização (latitude/longitude).
* **[Infra]** Implementação do modelo SQLAlchemy com FK para `users.id` e repositório concreto `AddressRepositoryImpl`.
* **[Aplicação]** Casos de Uso completos para a gestão de endereços (Create, Update, GetByUser, GetAll, Delete).
* **[Apresentação]** Schemas rigorosos no Pydantic barrando dados inválidos e endpoints FastAPI padronizados.
* **[Qualidade]** TDD de ponta a ponta. Testes de domínio, integração (repositório), orquestração (casos de uso) e E2E (API). 

## 🧠 Retrospectiva (O Como)
### ✅ O que funcionou bem?
* A reutilização da infraestrutura de testes (via `conftest.py`) acelerou drasticamente o desenvolvimento.
* As validações do Pydantic (como `min_length` para cidade e bairro) provaram o seu valor barrando bad requests nos testes E2E antes mesmo de acionarem a camada de negócio.

### ⚠️ Lições Aprendidas / Obstáculos
* **Tratamento de Updates Parciais:** Reforçamos o uso do `exclude_unset=True` no Pydantic ao atualizar dados para evitar sobrescrever campos não enviados com valores `None`.

---

## 📊 Status Final
* **Próximos Passos:** Iniciar a Sprint 03 focada na Entidade `ProducerProfile` (Perfil de Vendedor), mantendo a separação de responsabilidades (SRP) em relação à entidade `User`.

---
**Assinatura:** Mark Construtor & Matheus