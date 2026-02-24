import pytest

def test_deve_criar_endereco_via_api(client):
    # 1. Cria utilizador primeiro
    user_resp = client.post("/users/register", json={
        "email": "dono.endereco.api@agrolocal.com",
        "password": "senha_forte_123",
        "full_name": "Dono do Endereço"
    })
    user_id = user_resp.json()["id"]

    # 2. Cria endereço
    payload = {
        "user_id": user_id,
        "address_type": "RURAL",
        "street": "Estrada de Terra",
        "number": "S/N",
        "neighborhood": "Zona Rural",
        "city": "Interior",
        "state": "SP",
        "postal_code": "00000-000",
        "label": "Meu Sítio",
        "reference_point": "Perto da ponte"
    }
    response = client.post("/addresses/", json=payload)
    
    assert response.status_code == 201
    assert response.json()["street"] == "Estrada de Terra"
    assert response.json()["user_id"] == user_id
    assert response.json()["reference_point"] == "Perto da ponte"

def test_deve_listar_enderecos_do_usuario_via_api(client):
    # 1. Cria utilizador
    user_resp = client.post("/users/register", json={
        "email": "listar.endereco@agrolocal.com",
        "password": "senha_forte_123",
        "full_name": "Listador"
    })
    user_id = user_resp.json()["id"]

    # 2. Cria endereço
    client.post("/addresses/", json={
        "user_id": user_id,
        "street": "Rua Um", "number": "1", "neighborhood": "Bairro",
        "city": "Cidade", "state": "MG", "postal_code": "11111-111"
    })

    # 3. Busca endereços
    response = client.get(f"/addresses/user/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    assert data[0]["street"] == "Rua Um"

def test_deve_deletar_endereco_via_api(client):
    # 1. Cria utilizador e endereço
    user_resp = client.post("/users/register", json={
        "email": "deletar.endereco@agrolocal.com",
        "password": "senha_forte_123",
        "full_name": "Deletador"
    })
    user_id = user_resp.json()["id"]

    end_resp = client.post("/addresses/", json={
        "user_id": user_id,
        "street": "Rua X", 
        "number": "2", 
        "neighborhood": "Bairro Y", # <-- Aumentámos para passar no min_length=2
        "city": "Cidade Z",         # <-- Aumentámos para passar no min_length=2
        "state": "RJ", 
        "postal_code": "22222-222"
    })
    address_id = end_resp.json()["id"]

    # 2. Deleta
    del_resp = client.delete(f"/addresses/{address_id}")
    assert del_resp.status_code == 204

    # 3. Valida se sumiu da lista (Soft Delete)
    lista_resp = client.get(f"/addresses/user/{user_id}")
    assert len(lista_resp.json()) == 0
    
def test_deve_listar_todos_os_enderecos(client):
    response = client.get("/addresses/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_deve_atualizar_endereco_via_api(client):
    # 1. Cria utilizador e endereço
    user_resp = client.post("/users/register", json={
        "email": "update.end@agrolocal.com", "password": "senha_forte_123", "full_name": "Updator"
    })
    user_id = user_resp.json()["id"]

    end_resp = client.post("/addresses/", json={
        "user_id": user_id, "street": "Rua Velha", "number": "10", 
        "neighborhood": "Bairro Antigo", "city": "Cidade", "state": "SP", "postal_code": "00000-000"
    })
    address_id = end_resp.json()["id"]

    # 2. Atualiza (PUT)
    put_resp = client.put(f"/addresses/{address_id}", json={
        "street": "Rua Nova Reformada",
        "number": "20B"
    })
    
    # 3. Valida
    assert put_resp.status_code == 200
    assert put_resp.json()["street"] == "Rua Nova Reformada"
    assert put_resp.json()["number"] == "20B"
    assert put_resp.json()["city"] == "Cidade" # O que não atualizamos deve manter-se igual!