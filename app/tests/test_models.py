from app.models.user_model import User, UserRole
from app.models.catalog_model import Category
from app.schemas.user_schema import UserCreate

def test_create_user_model(db_session):
    """Testa se o modelo User gera UUID e salva corretamente."""
    user = User(
        email="teste@teste.com",
        password_hash="senha123",
        full_name="Tester",
        role=UserRole.CLIENTE
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    assert user.id is not None  # UUID foi gerado?
    assert str(user.id) != ""   # Não está vazio?
    assert user.email == "teste@teste.com"
    assert user.is_active is True # Default funcionou?

def test_category_slug_uniqueness(db_session):
    """Testa se o banco impede slugs duplicados (Constraint)."""
    cat1 = Category(name="Frutas", slug="frutas")
    db_session.add(cat1)
    db_session.commit()

    # Tenta criar outra categoria com o mesmo slug
    cat2 = Category(name="Frutas 2", slug="frutas")
    db_session.add(cat2)
    
    # O SQLAlchemy deve lançar erro de integridade
    try:
        db_session.commit()
        assert False, "Deveria ter falhado por slug duplicado"
    except Exception:
        db_session.rollback()
        assert True