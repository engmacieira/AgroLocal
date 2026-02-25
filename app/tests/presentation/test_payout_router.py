import pytest
import uuid

def test_jornada_de_repasse_financeiro_via_api(client):
    # 1. SETUP: Criar o cenário completo de venda (Usuários, Oferta, Checkout e Máquina de Estados)
    # Usuários
    cust_resp = client.post("/users/register", json={"email": "comprador_payout@teste.com", "password": "senha123", "full_name": "Comprador"})
    customer_id = cust_resp.json()["id"]
    
    prod_resp = client.post("/users/register", json={"email": "produtor_payout@teste.com", "password": "senha123", "full_name": "Pagador"})
    producer_id = prod_resp.json()["id"]
    client.post("/producers/", json={"user_id": producer_id, "store_name": "Lojinha", "document": "333", "pix_key": "pix@produtor.com"})
    
    # Oferta
    cat_resp = client.post("/catalog/categories/", json={"name": "Vegetais"})
    category_id = cat_resp.json()["id"]
    glob_resp = client.post("/catalog/products/suggest", json={"name": "Alface", "category_id": category_id})
    global_product_id = glob_resp.json()["id"]
    client.patch(f"/catalog/products/{global_product_id}/approve?admin_id={str(uuid.uuid4())}")
    
    offer_resp = client.post("/offers/", json={
        "producer_id": producer_id, "global_product_id": global_product_id, "price": 10.00, "stock_quantity": 50.0
    })
    offer_id = offer_resp.json()["id"]
    client.put(f"/offers/{offer_id}/delivery", json={"options": [{"delivery_type": "RETIRADA_PRODUTOR", "fee": 0.0}]})

    # Checkout
    checkout_resp = client.post("/orders/checkout", json={
        "customer_id": customer_id,
        "groups": [{"producer_id": producer_id, "delivery_type": "RETIRADA_PRODUTOR", "items": [{"offer_id": offer_id, "quantity": 10.0}]}]
    })
    pedido_id = checkout_resp.json()[0]["id"] # R$ 100.00 no total

    # Avançar Máquina de Estados até DELIVERED
    client.patch(f"/orders/{pedido_id}/status", json={"action": "PAID"})
    client.patch(f"/orders/{pedido_id}/status", json={"action": "PREPARING"})
    client.patch(f"/orders/{pedido_id}/status", json={"action": "READY"})
    client.patch(f"/orders/{pedido_id}/status", json={"action": "DELIVERED"})

    # ---------------------------------------------------------
    # 2. A JORNADA DE REPASSE (PAYOUT) COMEÇA AQUI
    # ---------------------------------------------------------

    # A. O Sistema (ou Admin) agenda o repasse cobrando 10%
    schedule_resp = client.post("/payouts/schedule", json={
        "order_id": pedido_id,
        "target_pix_key": "pix@produtor.com",
        "fee_percentage": 10.00
    })
    
    assert schedule_resp.status_code == 201
    repasse = schedule_resp.json()
    repasse_id = repasse["id"]
    
    assert repasse["status"] == "SCHEDULED"
    assert float(repasse["amount_gross"]) == 100.00
    assert float(repasse["amount_fee"]) == 10.00
    assert float(repasse["amount_net"]) == 90.00 # A nossa matemática a funcionar pela API!

    # B. O Admin faz a transferência no banco e processa no sistema
    process_resp = client.patch(f"/payouts/{repasse_id}/process", json={
        "bank_transaction_id": "PIX-COMPROVANTE-999",
        "proof_url": "https://agrolocal.com/recibos/999.pdf"
    })
    
    assert process_resp.status_code == 200
    assert process_resp.json()["status"] == "PAID"
    assert process_resp.json()["bank_transaction_id"] == "PIX-COMPROVANTE-999"

    # C. Verifica se o Pedido original avançou para COMPLETED!
    orders_resp = client.get(f"/orders/customer/{customer_id}")
    pedido_final = orders_resp.json()[0]
    assert pedido_final["status"] == "COMPLETED"