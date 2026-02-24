# 🗺️ Sprint 02: Gestão de Endereços (Address)

**Objetivo:** Implementar a entidade de Endereços com arquitetura DDD, permitindo que usuários gerenciem seus locais de entrega/retirada para a logística do AgroLocal.
**Status:** Planejamento
**Tecnologia Principal:** FastAPI, SQLAlchemy, Pytest (TDD)

---

## 🎯 Backlog de Funcionalidades (Escopo)
*Funcionalidades selecionadas para esta sprint, baseadas na necessidade de logística rural.*

### 📦 1. Módulo de Endereços (Contexto de Identidade/Logística)
* **[US-XX] Criar Endereço**
    * **O que é:** Permitir que o usuário logado adicione um novo endereço (Rua, Número, CEP, Cidade, Estado, Complemento).
    * **Critério de Aceite:** O endereço deve nascer vinculado obrigatoriamente a um `user_id` válido.
    * **Regra de Negócio:** Deve suportar coordenadas (Latitude/Longitude) de forma opcional, pois áreas rurais muitas vezes não possuem CEP preciso.

* **[US-XX] Listar Endereços do Usuário**
    * **O que é:** Buscar todos os endereços vinculados a um usuário específico.
    * **Critério de Aceite:** Retornar uma lista paginada de endereços ativos.

* **[US-XX] Atualizar Endereço**
    * **O que é:** Editar os dados de um endereço existente.
    * **Critério de Aceite:** Apenas o dono do endereço (ou admin) pode atualizá-lo.

* **[US-XX] Remover Endereço**
    * **O que é:** Apagar um endereço do catálogo do usuário.
    * **Regra de Negócio:** Deleção lógica (Soft Delete) ou bloqueio de deleção caso o endereço já esteja vinculado a um pedido em andamento (a definir na implementação dos casos de uso).

---

## 🛠️ Plano Técnico de Execução (Baby Steps / TDD)
*O passo a passo para garantirmos a fundação blindada.*

1.  **Testes de Domínio (RED):** Criar `app/tests/domain/test_address.py` para validar o nascimento da entidade e as regras de negócio de coordenadas/CEP.
2.  **Domínio (GREEN):** Criar `Address` (Entidade) e `IAddressRepository` (Contrato).
3.  **Infraestrutura:** Criar `AddressModel` (SQLAlchemy), implementar `AddressRepositoryImpl` e escrever os testes de integração usando nossa fixture do `conftest.py`.
4.  **Aplicação:** Criar `address_management.py` com os Casos de Uso (DTOs para Create, Update) e criar `test_address_use_cases.py` com nosso dublê (`FakeAddressRepository`).
5.  **Apresentação:** Criar `address_schema.py` (Pydantic V2) e `address_router.py` (FastAPI), validando o fluxo End-to-End com o `TestClient`.

---

## 📝 Definição de Pronto (DoD)
*Checklist para considerar a Sprint finalizada.*

* [ ] Código commited e pushado.
* [ ] Funcionalidades testadas localmente via Swagger UI.
* [ ] 100% de testes automatizados passando (Domínio, Infra, App e Presentation).
* [ ] Documentação (`Por_Onde_Comecar.md` e Logs) atualizada.