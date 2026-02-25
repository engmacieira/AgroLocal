import pytest
import uuid

def test_jornada_completa_de_pagamento_via_api(client):
    # 1. SETUP GIGANTE (Igual ao do Checkout para termos um pedido real no banco)
    cust_resp = client.post("/users/register", json={"email": "pagador@teste.com", "password": "senha123", "full_name": "Pagador"})
    customer_id = cust_resp.json()["id"]
    
    prod_resp = client.post("/users/register", json={"email": "recebedor@teste.com", "password": "senha123", "full_name": "Recebedor"})
    producer_id = prod_resp.json()["id"]
    client.post("/producers/", json={"user_id": producer_id, "store_name": "Sitio", "document": "222", "pix_key": "pix"})
    
    cat_resp = client.post("/catalog/categories/", json={"name": "Frutas API"})
    category_id = cat_resp.json()["id"]
    glob_resp = client.post("/catalog/products/suggest", json={"name": "Banana Prata", "category_id": category_id})
    global_product_id = glob_resp.json()["id"]
    client.patch(f"/catalog/products/{global_product_id}/approve?admin_id={str(uuid.uuid4())}")
    
    offer_resp = client.post("/offers/", json={
        "producer_id": producer_id, "global_product_id": global_product_id, "price": 10.00, "stock_quantity": 50.0
    })
    offer_id = offer_resp.json()["id"]
    client.put(f"/offers/{offer_id}/delivery", json={"options": [{"delivery_type": "RETIRADA_PRODUTOR", "fee": 0.0}]})

    # Faz o Checkout para gerar o Pedido
    checkout_resp = client.post("/orders/checkout", json={
        "customer_id": customer_id,
        "groups": [{"producer_id": producer_id, "delivery_type": "RETIRADA_PRODUTOR", "items": [{"offer_id": offer_id, "quantity": 2.0}]}]
    })
    pedido_id = checkout_resp.json()[0]["id"]

    # ---------------------------------------------------------
    # 2. A JORNADA FINANCEIRA COMEÇA AQUI
    # ---------------------------------------------------------

    # A. O cliente clica em "Pagar com PIX"
    pay_resp = client.post("/transactions/", json={
        "order_ids": [pedido_id],
        "payment_method": "PIX"
    })
    assert pay_resp.status_code == 201
    transacao = pay_resp.json()
    transacao_id = transacao["id"]
    
    assert transacao["status"] == "PENDING"
    assert float(transacao["amount"]) == 20.00 # 2 x 10.00
    assert "br.gov.bcb.pix" in transacao["pix_copy_paste"]

    # B. O cliente paga no app do banco e o Gateway (MercadoPago) bate no nosso Webhook
    webhook_resp = client.post(f"/transactions/{transacao_id}/webhook", json={
        "external_transaction_id": "MP-ABC-123",
        "is_approved": True
    })
    assert webhook_resp.status_code == 200
    assert webhook_resp.json()["status"] == "APPROVED"

    # C. Verifica se o pedido original mudou o status automaticamente para PAID!
    orders_resp = client.get(f"/orders/customer/{customer_id}")
    pedido_atualizado = orders_resp.json()[0]
    assert pedido_atualizado["id"] == pedido_id
    assert pedido_atualizado["status"] == "PAID"