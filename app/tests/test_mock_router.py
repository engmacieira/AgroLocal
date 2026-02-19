from fastapi.testclient import TestClient
from app.main import app

# Cria um cliente de teste que "finge" ser um navegador/app
client = TestClient(app)

# Prefixo das rotas de mock
PREFIX = "/mocks"

def test_mock_auth_login():
    """Testa se o login fake retorna o token esperado."""
    response = client.post(f"{PREFIX}/auth/login")
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user_role"] == "PRODUTOR"

def test_mock_get_my_profile():
    """Testa se o perfil traz os dados do usuário E do produtor aninhados."""
    response = client.get(f"{PREFIX}/users/me")
    assert response.status_code == 200
    data = response.json()
    
    # Valida campos do User
    assert data["email"] == "joao@fazenda.com"
    assert "id" in data
    
    # Valida objeto aninhado (ProducerProfile)
    assert data["producer_profile"] is not None
    assert data["producer_profile"]["store_name"] == "Sítio Recanto Verde"
    assert "rating" in data["producer_profile"]

def test_mock_get_addresses():
    """Testa a listagem de endereços."""
    response = client.get(f"{PREFIX}/users/me/addresses")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert data[0]["state"] == "SP"
    assert "latitude" in data[0]

def test_mock_vitrine_flow():
    """
    Testa o fluxo da Vitrine: Categorias -> Produtos.
    Garante que a estrutura da 'Home' do App não quebrou.
    """
    # 1. Busca Categorias
    resp_cat = client.get(f"{PREFIX}/categories")
    assert resp_cat.status_code == 200
    cats = resp_cat.json()
    assert len(cats) >= 3
    assert "icon_url" in cats[0]

    # 2. Busca Ofertas (Produtos)
    resp_prod = client.get(f"{PREFIX}/products/offers")
    assert resp_prod.status_code == 200
    prods = resp_prod.json()
    assert len(prods) > 0
    
    # Valida Eager Loading (Produto Global dentro da Oferta)
    first_offer = prods[0]
    assert "global_info" in first_offer
    assert "name" in first_offer["global_info"]
    assert "images" in first_offer
    assert isinstance(first_offer["price"], (str, float)) # JSON retorna Decimal como string ou float

def test_mock_checkout_flow():
    """
    Testa o fluxo crítico de Checkout: Criar Pedido -> Gerar PIX.
    """
    # 1. Criar Pedido (Mock aceita qualquer payload válido pelo schema)
    payload = {
        "producer_id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
        "items": [
            {"product_id": "b2f4c810-1d2a-4f5b-9c8e-2a3b4c5d6e7f", "quantity": 1.5}
        ],
        "delivery_type": "RETIRADA",
        "delivery_address_snapshot": "Rua Teste, 123"
    }
    resp_order = client.post(f"{PREFIX}/orders", json=payload)
    assert resp_order.status_code == 201
    assert "order_id" in resp_order.json()

    # 2. Gerar Pagamento (Transaction)
    tx_payload = {
        "order_id": resp_order.json()["order_id"],
        "payment_method": "PIX",
        "amount": 50.00,
        "installments": 1
    }
    resp_tx = client.post(f"{PREFIX}/transactions", json=tx_payload)
    assert resp_tx.status_code == 200
    tx_data = resp_tx.json()
    
    # O MAIS IMPORTANTE: O Frontend precisa desses campos para exibir o QR Code!
    assert "pix_qr_code_base64" in tx_data
    assert "pix_copy_paste" in tx_data
    assert tx_data["status"] == "PENDING"

def test_mock_financial_dashboard():
    """Testa se o painel financeiro traz os repasses."""
    response = client.get(f"{PREFIX}/payouts")
    assert response.status_code == 200
    payouts = response.json()
    assert len(payouts) > 0
    assert "amount_net" in payouts[0]
    assert "status" in payouts[0]