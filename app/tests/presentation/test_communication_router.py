import pytest
import uuid

def test_jornada_completa_de_comunicacao_via_api(client):
    # 1. SETUP: Criar utilizadores
    cust_resp = client.post("/users/register", json={"email": "cliente_ticket@teste.com", "password": "123456789", "full_name": "Cliente"})
    customer_id = cust_resp.json()["id"]
    
    prod_resp = client.post("/users/register", json={"email": "produtor_ticket@teste.com", "password": "123456789", "full_name": "Produtor"})
    producer_id = prod_resp.json()["id"]

    # ---------------------------------------------------------
    # 2. ABRIR O CHAMADO (O cliente inicia a conversa)
    # ---------------------------------------------------------
    start_resp = client.post("/conversations/", json={
        "initiator_id": customer_id,
        "target_id": producer_id,
        "subject_type": "PRODUCT_QUESTION",
        "initiator_role": "CUSTOMER",
        "target_role": "PRODUCER",
        "initial_message": "Olá, os morangos são orgânicos?"
    })
    
    assert start_resp.status_code == 201
    conversa = start_resp.json()
    conversa_id = conversa["id"]
    
    assert conversa["status"] == "OPEN"
    assert len(conversa["messages"]) == 1
    assert conversa["messages"][0]["content"] == "Olá, os morangos são orgânicos?"

    # ---------------------------------------------------------
    # 3. RESPONDER O CHAMADO (O produtor responde)
    # ---------------------------------------------------------
    reply_resp = client.post(f"/conversations/{conversa_id}/messages", json={
        "sender_id": producer_id,
        "sender_role": "PRODUCER",
        "content": "Sim! 100% orgânicos e sem agrotóxicos."
    })
    
    assert reply_resp.status_code == 200
    assert len(reply_resp.json()["messages"]) == 2
    assert reply_resp.json()["messages"][1]["content"] == "Sim! 100% orgânicos e sem agrotóxicos."

    # ---------------------------------------------------------
    # 4. LISTAR CAIXA DE ENTRADA (O cliente vê as suas conversas)
    # ---------------------------------------------------------
    inbox_resp = client.get(f"/conversations/user/{customer_id}")
    assert inbox_resp.status_code == 200
    assert len(inbox_resp.json()) == 1
    assert inbox_resp.json()[0]["id"] == conversa_id

    # ---------------------------------------------------------
    # 5. ENCERRAR E TESTAR BLOQUEIO (Auditoria)
    # ---------------------------------------------------------
    close_resp = client.patch(f"/conversations/{conversa_id}/close")
    assert close_resp.status_code == 200
    assert close_resp.json()["status"] == "CLOSED"

    # Tenta mandar mensagem com chamado fechado (Deve falhar)
    fail_reply = client.post(f"/conversations/{conversa_id}/messages", json={
        "sender_id": customer_id, "sender_role": "CUSTOMER", "content": "Obrigado!"
    })
    assert fail_reply.status_code == 400
    assert "fechada" in fail_reply.json()["detail"].lower()