import pytest

def test_jornada_completa_de_oferta_via_api(client):
    # 1. Setup: Cria User
    user_resp = client.post("/users/register", json={
        "email": "agricultor.feliz@agrolocal.com", "password": "senha_forte", "full_name": "Agricultor"
    })
    user_id = user_resp.json()["id"]

    # 2. Setup: Cria Producer
    prod_resp = client.post("/producers/", json={
        "user_id": user_id, "store_name": "Sitio Feliz", "document": "99887766554", "pix_key": "pixsitio"
    })
    producer_id = prod_resp.json()["id"]

    # 3. Setup: Cria Category
    cat_resp = client.post("/catalog/categories/", json={"name": "Hortifruti"})
    category_id = cat_resp.json()["id"]

    # 4. Setup: Cria Global Product
    glob_resp = client.post("/catalog/products/suggest", json={
        "name": "Cebola Roxa", "category_id": category_id
    })
    global_product_id = glob_resp.json()["id"]

    # --- INÍCIO DOS TESTES DE OFERTA ---

    # A) Criar a Oferta
    offer_resp = client.post("/offers/", json={
        "producer_id": producer_id,
        "global_product_id": global_product_id,
        "price": 8.50, # Será convertido em Decimal
        "unit": "kg",
        "stock_quantity": 50.0
    })
    
    assert offer_resp.status_code == 201
    assert offer_resp.json()["stock_quantity"] == 50.0
    offer_id = offer_resp.json()["id"]

    # B) Atualizar o Estoque (+ 20.5 kg colhidos hoje)
    stock_resp = client.patch(f"/offers/{offer_id}/stock", json={
        "add_quantity": 20.5
    })
    assert stock_resp.status_code == 200
    assert stock_resp.json()["stock_quantity"] == 70.5

    # C) Atualizar Detalhes (Subir o preço)
    from decimal import Decimal
    
    det_resp = client.patch(f"/offers/{offer_id}/details", json={
        "new_price": 9.90
    })
    assert det_resp.status_code == 200
    
    # Comparamos matematicamente convertendo a resposta para Decimal!
    assert Decimal(det_resp.json()["price"]) == Decimal("9.90")

    # D) Listar Vitrine do Produtor
    list_resp = client.get(f"/offers/producer/{producer_id}")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1
    assert Decimal(list_resp.json()[0]["price"]) == Decimal("9.90")
    
def test_deve_adicionar_logistica_e_imagem_na_oferta_via_api(client):
    # Setup Rápido (Cria User -> Producer -> Categoria -> Produto -> Oferta)
    user_resp = client.post("/users/register", json={"email": "logistica@agrolocal.com", "password": "senha123", "full_name": "Log"})
    user_id = user_resp.json()["id"]
    
    prod_resp = client.post("/producers/", json={"user_id": user_id, "store_name": "Log", "document": "00000000000", "pix_key": "pix123456"})
    producer_id = prod_resp.json()["id"]
    
    cat_resp = client.post("/catalog/categories/", json={"name": "Logistica"})
    category_id = cat_resp.json()["id"]
    
    glob_resp = client.post("/catalog/products/suggest", json={"name": "Alho", "category_id": category_id})
    global_product_id = glob_resp.json()["id"]
    
    offer_resp = client.post("/offers/", json={
        "producer_id": producer_id, "global_product_id": global_product_id, "price": 2.00, "unit": "cabeça"
    })
    offer_id = offer_resp.json()["id"]

    # 1. Testa Adição de Opções de Entrega (PUT)
    delivery_resp = client.put(f"/offers/{offer_id}/delivery", json={
        "options": [
            {"delivery_type": "DOMICILIO", "fee": 5.50, "schedule": "Sábados"},
            {"delivery_type": "RETIRADA_PRODUTOR", "fee": 0.0, "schedule": "Diariamente"}
        ]
    })
    
    assert delivery_resp.status_code == 200
    assert len(delivery_resp.json()["delivery_options"]) == 2
    assert delivery_resp.json()["delivery_options"][0]["delivery_type"] == "DOMICILIO"

    # 2. Testa Adição de Imagem (POST)
    image_resp = client.post(f"/offers/{offer_id}/images", json={
        "url": "http://s3.aws.com/foto_alho.jpg",
        "is_primary": True
    })
    
    assert image_resp.status_code == 200
    assert len(image_resp.json()["images"]) == 1
    assert image_resp.json()["images"][0]["url"] == "http://s3.aws.com/foto_alho.jpg"