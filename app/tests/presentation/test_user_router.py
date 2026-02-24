import pytest

# 🌟 MAGIA DO PYTEST:
# Não precisamos importar o TestClient, o Base, nem o engine aqui.
# Como criamos o 'conftest.py', o Pytest automaticamente encontra a fixture 'client'
# e a injeta em todas as funções abaixo! O código fica 100% DRY.

def test_deve_registrar_usuario_via_api_com_sucesso(client):
    payload = {
        "email": "cliente.api@agrolocal.com",
        "password": "senha_forte_123",
        "full_name": "Consumidor API",
        "role": "CLIENTE"
    }
    
    response = client.post("/users/register", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "cliente.api@agrolocal.com"
    assert "id" in data
    assert "password" not in data

def test_nao_deve_permitir_email_duplicado_via_api(client):
    # 1. Cria o primeiro usuário
    payload_original = {
        "email": "duplicado@agrolocal.com",
        "password": "senha_forte_123",
        "full_name": "Original"
    }
    client.post("/users/register", json=payload_original)
    
    # 2. Tenta registrar um SEGUNDO usuário com o MESMO e-mail
    payload_copia = {
        "email": "duplicado@agrolocal.com",
        "password": "outra_senha",
        "full_name": "Copião"
    }
    response = client.post("/users/register", json=payload_copia)
    
    # 3. Agora sim, deve barrar!
    assert response.status_code == 400
    assert response.json()["detail"] == "Email já está em uso"

def test_pydantic_deve_bloquear_senha_curta(client):
    payload = {
        "email": "novo@agrolocal.com",
        "password": "123", 
        "full_name": "Teste Validação"
    }
    response = client.post("/users/register", json=payload)
    assert response.status_code == 422 
    
def test_deve_listar_todos_os_usuarios(client):
    response = client.get("/users/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_deve_buscar_usuario_por_id_e_atualizar(client):
    cria_response = client.post("/users/register", json={
        "email": "update@agrolocal.com",
        "password": "senha123",
        "full_name": "Antigo Nome"
    })
    user_id = cria_response.json()["id"]

    busca_response = client.get(f"/users/{user_id}")
    assert busca_response.status_code == 200
    assert busca_response.json()["full_name"] == "Antigo Nome"

    update_response = client.put(f"/users/{user_id}", json={
        "full_name": "Novo Nome Atualizado",
        "phone": "11999999999"
    })
    assert update_response.status_code == 200
    assert update_response.json()["full_name"] == "Novo Nome Atualizado"
    
def test_deve_aplicar_soft_delete_via_api(client):
    cria_response = client.post("/users/register", json={
        "email": "deletar_api@agrolocal.com",
        "password": "senha123",
        "full_name": "Vai Sumir"
    })
    user_id = cria_response.json()["id"]

    delete_response = client.delete(f"/users/{user_id}")
    assert delete_response.status_code == 204

    busca_response = client.get(f"/users/{user_id}")
    assert busca_response.status_code == 200
    assert busca_response.json()["is_active"] is False

def test_deve_fazer_login_com_sucesso(client):
    client.post("/users/register", json={
        "email": "login@agrolocal.com",
        "password": "senha_forte",
        "full_name": "Testador Login"
    })

    login_response = client.post("/users/login", json={
        "email": "login@agrolocal.com",
        "password": "senha_forte"
    })
    
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()

def test_nao_deve_fazer_login_com_senha_errada(client):
    login_response = client.post("/users/login", json={
        "email": "login@agrolocal.com",
        "password": "senha_errada_123"
    })
    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Credenciais inválidas"

def test_deve_aceitar_termos_e_verificar_conta(client):
    cria_response = client.post("/users/register", json={
        "email": "acoes@agrolocal.com",
        "password": "senha_forte",
        "full_name": "Testador Ações"
    })
    user_id = cria_response.json()["id"]

    terms_response = client.patch(f"/users/{user_id}/accept-terms")
    assert terms_response.status_code == 204

    verify_response = client.patch(f"/users/{user_id}/verify")
    assert verify_response.status_code == 204

    busca_response = client.get(f"/users/{user_id}")
    assert busca_response.json()["is_verified"] is True