import pytest
import uuid

def test_jornada_de_checkout_via_api(client):
    # 1. SETUP GIGANTE (A preparação do palco)
    # Criar Cliente
    cust_resp = client.post("/users/register", json={"email": "comprador@teste.com", "password": "senha123", "full_name": "Comprador"})
    customer_id = cust_resp.json()["id"]
    
    # Criar Produtor
    prod_resp = client.post("/users/register", json={"email": "fazendeiro@teste.com", "password": "senha123", "full_name": "Fazendeiro"})
    user_prod_id = prod_resp.json()["id"]
    client.post("/producers/", json={"user_id": user_prod_id, "store_name": "Sitio", "document": "111", "pix_key": "pix"})
    
    # Criar Produto no Catálogo (Aprovado direto para facilitar o teste)
    cat_resp = client.post("/catalog/categories/", json={"name": "Hortaliças"})
    category_id = cat_resp.json()["id"]
    glob_resp = client.post("/catalog/products/suggest", json={"name": "Cenoura", "category_id": category_id})
    global_product_id = glob_resp.json()["id"]
    client.patch(f"/catalog/products/{global_product_id}/approve?admin_id={str(uuid.uuid4())}")
    
    # Criar Oferta
    offer_resp = client.post("/offers/", json={
        "producer_id": user_prod_id, "global_product_id": global_product_id, 
        "price": 5.00, "unit": "kg", "stock_quantity": 20.0
    })
    offer_id = offer_resp.json()["id"]
    
    # Adicionar Frete à Oferta
    client.put(f"/offers/{offer_id}/delivery", json={
        "options": [{"delivery_type": "DOMICILIO", "fee": 10.00}]
    })

    # 2. ACT: O CHECKOUT (O cliente compra 3kg de cenoura)
    checkout_payload = {
        "customer_id": customer_id,
        "groups": [
            {
                "producer_id": user_prod_id,
                "delivery_type": "DOMICILIO",
                "items": [
                    {"offer_id": offer_id, "quantity": 3.0}
                ]
            }
        ]
    }
    
    checkout_resp = client.post("/orders/checkout", json=checkout_payload)
    
    # 3. ASSERT (Validações)
    assert checkout_resp.status_code == 201
    pedidos = checkout_resp.json()
    assert len(pedidos) == 1
    
    pedido = pedidos[0]
    assert pedido["status"] == "CREATED"
    # Preço: (3kg * 5.00) + 10.00 Frete = 25.00
    assert float(pedido["total_amount"]) == 25.00 
    assert pedido["delivery_fee"] == "10.00"
    assert len(pedido["items"]) == 1
    assert pedido["items"][0]["product_name_snapshot"] == "Cenoura"

    # Confirma reserva de estoque buscando a oferta novamente
    offer_check = client.get(f"/offers/producer/{user_prod_id}")
    assert offer_check.json()[0]["stock_quantity"] == 17.0 # 20 inicial - 3 vendidos
    
    # 4. A JORNADA DO PÓS-VENDA (Máquina de Estados)
    pedido_id = pedido["id"]

    # Passo A: Cliente Pagou
    paid_resp = client.patch(f"/orders/{pedido_id}/status", json={"action": "PAID"})
    assert paid_resp.status_code == 200
    assert paid_resp.json()["status"] == "PAID"

    # Passo B: Produtor a separar os vegetais
    prep_resp = client.patch(f"/orders/{pedido_id}/status", json={"action": "PREPARING"})
    assert prep_resp.status_code == 200
    assert prep_resp.json()["status"] == "PREPARING"

    # Passo C: Pronto para entrega/retirada
    ready_resp = client.patch(f"/orders/{pedido_id}/status", json={"action": "READY"})
    assert ready_resp.status_code == 200
    assert ready_resp.json()["status"] == "READY"

    # Passo D: Entregue ao cliente!
    deliv_resp = client.patch(f"/orders/{pedido_id}/status", json={"action": "DELIVERED"})
    assert deliv_resp.status_code == 200
    assert deliv_resp.json()["status"] == "DELIVERED"
    
    # Passo E: Tentativa de Cancelamento (Prova de que a Regra de Negócio funciona)
    # Tenta cancelar um pedido que já foi entregue
    cancel_resp = client.patch(f"/orders/{pedido_id}/status", json={"action": "CANCELED", "reason": "Desisti de comer"})
    assert cancel_resp.status_code == 400
    assert "Não é possível cancelar um pedido já entregue" in cancel_resp.json()["detail"]