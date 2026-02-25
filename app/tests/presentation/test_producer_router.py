import pytest

def test_deve_criar_produtor_via_api(client):
    # 1. Cria utilizador base
    user_resp = client.post("/users/register", json={
        "email": "vendedor.api@agrolocal.com", "password": "senha_forte_123", "full_name": "Agricultor"
    })
    user_id = user_resp.json()["id"]

    # 2. Cria produtor
    prod_resp = client.post("/producers/", json={
        "user_id": user_id,
        "store_name": "Fazenda do Sol",
        "document": "12345678901",
        "pix_key": "fazenda@pix.com",
        "bio": "Produtos 100% orgânicos"
    })
    
    assert prod_resp.status_code == 201
    assert prod_resp.json()["rating"] == 5.0
    assert prod_resp.json()["store_name"] == "Fazenda do Sol"

def test_api_deve_bloquear_dois_perfis_para_mesmo_usuario(client):
    # 1. Cria utilizador base
    user_resp = client.post("/users/register", json={
        "email": "ganancioso@agrolocal.com", "password": "senha_forte", "full_name": "Duas Lojas"
    })
    user_id = user_resp.json()["id"]

    # 2. Cria a primeira loja (Ajustamos a pix_key para ter 5+ caracteres)
    client.post("/producers/", json={
        "user_id": user_id, "store_name": "Loja 1", "document": "11111111111", "pix_key": "chavepix1"
    })

    # 3. Tenta criar a segunda loja
    erro_resp = client.post("/producers/", json={
        "user_id": user_id, "store_name": "Loja 2", "document": "22222222222", "pix_key": "chavepix2"
    })
    
    assert erro_resp.status_code == 400
    assert erro_resp.json()["detail"] == "Usuário já possui um perfil de produtor ativo"

def test_deve_atualizar_dados_da_vitrine_via_api(client):
    # 1. Cria utilizador e produtor (Ajustamos a senha para 6+ caracteres)
    user_resp = client.post("/users/register", json={
        "email": "update.loja@agrolocal.com", "password": "senha123", "full_name": "Update"
    })
    user_id = user_resp.json()["id"]

    # Ajustamos a pix_key também
    client.post("/producers/", json={
        "user_id": user_id, "store_name": "Loja Velha", "document": "33333333333", "pix_key": "chavepix3"
    })

    # 2. Atualiza via PUT (mudando apenas o nome)
    put_resp = client.put(f"/producers/user/{user_id}", json={
        "store_name": "Loja Nova e Reformada"
    })
    
    assert put_resp.status_code == 200
    assert put_resp.json()["store_name"] == "Loja Nova e Reformada"
    assert put_resp.json()["document"] == "33333333333"
    
def test_deve_listar_todos_produtores_ativos(client):
    response = client.get("/producers/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_deve_desativar_produtor_via_api(client):
    # 1. Cria utilizador e produtor
    user_resp = client.post("/users/register", json={
        "email": "delete.loja@agrolocal.com", "password": "senha_forte", "full_name": "Delete"
    })
    user_id = user_resp.json()["id"]

    prod_resp = client.post("/producers/", json={
        "user_id": user_id, "store_name": "Loja Que Vai Sumir", 
        "document": "99988877766", "pix_key": "pixdelete"
    })
    profile_id = prod_resp.json()["id"]

    # 2. Deleta via API (DELETE)
    del_resp = client.delete(f"/producers/{profile_id}")
    assert del_resp.status_code == 204 # No Content

    # 3. Verifica se sumiu da busca individual (pois a busca filtra apenas ativos)
    busca_resp = client.get(f"/producers/user/{user_id}")
    assert busca_resp.status_code == 404 # Not Found