import pytest
import uuid

def test_jornada_completa_de_avaliacao_via_api(client):
    # 1. SETUP GIGANTE: Criar a venda completa
    cust_resp = client.post("/users/register", json={"email": "cliente_review@teste.com", "password": "senha123", "full_name": "Cliente"})
    customer_id = cust_resp.json()["id"]
    
    prod_resp = client.post("/users/register", json={"email": "prod_review@teste.com", "password": "senha123", "full_name": "Produtor"})
    producer_id = prod_resp.json()["id"]
    client.post("/producers/", json={"user_id": producer_id, "store_name": "S", "document": "444", "pix_key": "pix"})
    
    cat_resp = client.post("/catalog/categories/", json={"name": "Laticínios"})
    category_id = cat_resp.json()["id"]
    glob_resp = client.post("/catalog/products/suggest", json={"name": "Queijo Minas", "category_id": category_id})
    global_product_id = glob_resp.json()["id"]
    client.patch(f"/catalog/products/{global_product_id}/approve?admin_id={str(uuid.uuid4())}")
    
    offer_resp = client.post("/offers/", json={
        "producer_id": producer_id, "global_product_id": global_product_id, "price": 40.00, "stock_quantity": 10.0
    })
    offer_id = offer_resp.json()["id"]
    client.put(f"/offers/{offer_id}/delivery", json={"options": [{"delivery_type": "RETIRADA_PRODUTOR", "fee": 0.0}]})

    # Checkout
    checkout_resp = client.post("/orders/checkout", json={
        "customer_id": customer_id,
        "groups": [{"producer_id": producer_id, "delivery_type": "RETIRADA_PRODUTOR", "items": [{"offer_id": offer_id, "quantity": 1.0}]}]
    })
    pedido_id = checkout_resp.json()[0]["id"]

    # ---------------------------------------------------------
    # 2. A TENTATIVA PREMATURA (O cliente tenta avaliar antes de receber)
    # ---------------------------------------------------------
    fail_review = client.post("/reviews/", json={
        "order_id": pedido_id, "customer_id": customer_id, "rating": 5
    })
    assert fail_review.status_code == 400
    assert "Apenas pedidos entregues" in fail_review.json()["detail"]

    # ---------------------------------------------------------
    # 3. AVALIAÇÃO COM SUCESSO (Avança a ordem para entregue e avalia)
    # ---------------------------------------------------------
    client.patch(f"/orders/{pedido_id}/status", json={"action": "PAID"})
    client.patch(f"/orders/{pedido_id}/status", json={"action": "PREPARING"})
    client.patch(f"/orders/{pedido_id}/status", json={"action": "READY"})
    client.patch(f"/orders/{pedido_id}/status", json={"action": "DELIVERED"})

    success_review = client.post("/reviews/", json={
        "order_id": pedido_id, 
        "customer_id": customer_id, 
        "rating": 5,
        "comment": "Melhor queijo da região!",
        "photo_url": "https://img.com/queijo.jpg"
    })
    
    assert success_review.status_code == 201
    assert success_review.json()["rating"] == 5
    assert success_review.json()["comment"] == "Melhor queijo da região!"
    assert success_review.json()["photo_url"] == "https://img.com/queijo.jpg"

    # ---------------------------------------------------------
    # 4. A VITRINE DO PRODUTOR (O Frontend carrega as avaliações)
    # ---------------------------------------------------------
    vitrine_resp = client.get(f"/reviews/producer/{producer_id}")
    assert vitrine_resp.status_code == 200
    assert len(vitrine_resp.json()) == 1
    assert vitrine_resp.json()[0]["comment"] == "Melhor queijo da região!"