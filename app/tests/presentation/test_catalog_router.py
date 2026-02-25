import pytest
import uuid

def test_deve_criar_e_listar_categoria_via_api(client):
    # 1. Cria categoria
    post_resp = client.post("/catalog/categories/", json={
        "name": "Hortaliças Orgânicas",
        "icon_url": "http://img.com/folha.png"
    })
    assert post_resp.status_code == 201
    assert post_resp.json()["slug"] == "hortalicas-organicas" # Valida a inteligência do slug!

    # 2. Lista categorias
    get_resp = client.get("/catalog/categories/")
    assert get_resp.status_code == 200
    assert len(get_resp.json()) > 0

def test_deve_sugerir_e_aprovar_produto_via_api(client):
    admin_id = str(uuid.uuid4())
    
    # 1. Cria uma Categoria Base
    cat_resp = client.post("/catalog/categories/", json={"name": "Frutas Naturais"})
    category_id = cat_resp.json()["id"]

    # 2. Sugere um novo produto
    sug_resp = client.post("/catalog/products/suggest", json={
        "name": "Banana Nanica",
        "category_id": category_id,
        "ncm_code": "08039000"
    })
    
    assert sug_resp.status_code == 201
    assert sug_resp.json()["status"] == "PENDING"
    product_id = sug_resp.json()["id"]

    # 3. Admin Aprova o produto (Passando admin_id via Query Params)
    app_resp = client.patch(f"/catalog/products/{product_id}/approve?admin_id={admin_id}")
    
    assert app_resp.status_code == 200
    assert app_resp.json()["status"] == "APPROVED"

def test_deve_rejeitar_produto_com_motivo_via_api(client):
    admin_id = str(uuid.uuid4())
    
    cat_resp = client.post("/catalog/categories/", json={"name": "Grãos"})
    category_id = cat_resp.json()["id"]

    sug_resp = client.post("/catalog/products/suggest", json={
        "name": "Feijão Preto (Duplicado)",
        "category_id": category_id
    })
    product_id = sug_resp.json()["id"]

    # Admin Rejeita o produto (Passando payload com reason)
    rej_resp = client.patch(f"/catalog/products/{product_id}/reject", json={
        "admin_id": admin_id,
        "reason": "Produto já existe no catálogo como Feijão Preto"
    })
    
    assert rej_resp.status_code == 200
    assert rej_resp.json()["status"] == "REJECTED"
    assert rej_resp.json()["rejection_reason"] == "Produto já existe no catálogo como Feijão Preto"
    
def test_deve_listar_produtos_aprovados_por_categoria_via_api(client):
    # 1. Cria Categoria
    cat_resp = client.post("/catalog/categories/", json={"name": "Verduras"})
    category_id = cat_resp.json()["id"]

    # 2. Sugere Produto
    sug_resp = client.post("/catalog/products/suggest", json={"name": "Alface", "category_id": category_id})
    product_id = sug_resp.json()["id"]

    # 3. Admin aprova o produto
    client.patch(f"/catalog/products/{product_id}/approve?admin_id={str(uuid.uuid4())}")

    # 4. Busca pela categoria
    lista_resp = client.get(f"/catalog/categories/{category_id}/products")
    
    assert lista_resp.status_code == 200
    assert len(lista_resp.json()) == 1
    assert lista_resp.json()[0]["name"] == "Alface"

def test_deve_listar_produtos_pendentes_para_admin_via_api(client):
    # 1. Cria Categoria
    cat_resp = client.post("/catalog/categories/", json={"name": "Temperos"})
    category_id = cat_resp.json()["id"]

    # 2. Sugere Produto (Nasce PENDING)
    client.post("/catalog/products/suggest", json={"name": "Orégano", "category_id": category_id})

    # 3. Admin busca a fila de pendentes
    lista_resp = client.get("/catalog/products/status/PENDING")
    
    assert lista_resp.status_code == 200
    assert isinstance(lista_resp.json(), list)
    # Valida se o "Orégano" está na lista de pendentes devolvida
    assert any(p["name"] == "Orégano" for p in lista_resp.json())