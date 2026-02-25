import pytest
import uuid
from app.domain.entities.review import Review

def test_deve_criar_avaliacao_valida_com_comentario_e_foto():
    avaliacao = Review(
        order_id=uuid.uuid4(),
        customer_id=uuid.uuid4(),
        producer_id=uuid.uuid4(),
        rating=5,
        comment="Tomates incrivelmente frescos! Fizeram uma salada ótima.",
        photo_url="https://s3.amazonaws.com/agrolocal/reviews/foto_tomate.jpg"
    )
    
    assert avaliacao.rating == 5
    assert "Tomates incrivelmente" in avaliacao.comment
    assert avaliacao.photo_url.endswith(".jpg")

def test_nao_deve_aceitar_nota_fora_do_limite_1_a_5():
    # Nota maior que 5
    with pytest.raises(ValueError, match="A nota deve ser um número inteiro entre 1 e 5"):
        Review(order_id=uuid.uuid4(), customer_id=uuid.uuid4(), producer_id=uuid.uuid4(), rating=6)
        
    # Nota menor que 1
    with pytest.raises(ValueError, match="A nota deve ser um número inteiro entre 1 e 5"):
        Review(order_id=uuid.uuid4(), customer_id=uuid.uuid4(), producer_id=uuid.uuid4(), rating=0)

def test_deve_higienizar_comentario_vazio_apenas_com_espacos():
    avaliacao = Review(
        order_id=uuid.uuid4(),
        customer_id=uuid.uuid4(),
        producer_id=uuid.uuid4(),
        rating=4,
        comment="   \n   " # O utilizador só enviou espaços e quebras de linha
    )
    
    assert avaliacao.comment is None # O domínio limpou a "sujeira"
    assert avaliacao.photo_url is None # Foto também deve ser opcional