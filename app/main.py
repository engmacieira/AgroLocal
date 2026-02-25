from fastapi import FastAPI
from app.core.database import Base, engine
from app.presentation.routers import user_router
from app.presentation.routers import address_router
from app.presentation.routers import producer_router
from app.presentation.routers import catalog_router
from app.presentation.routers import offer_router
from app.presentation.routers import order_router
from app.presentation.routers import transaction_router
from app.presentation.routers import payout_router
from app.presentation.routers import review_router
from app.presentation.routers import communication_router

# Cria as tabelas no banco de dados local.
# Em um cenário 100% focado em produção, usaríamos o Alembic para isso,
# mas para testarmos nossa primeira fatia vertical localmente, isso é perfeito.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AgroLocal API",
    description="API com Arquitetura DDD para o marketplace da agricultura familiar."
)

# Conecta o nosso roteador de usuários à aplicação principal
app.include_router(user_router.router)
app.include_router(address_router.router)
app.include_router(producer_router.router)
app.include_router(catalog_router.router)
app.include_router(offer_router.router)
app.include_router(order_router.router)
app.include_router(transaction_router.router)
app.include_router(payout_router.router)
app.include_router(review_router.router)
app.include_router(communication_router.router)

@app.get("/")
def read_root():
    return {"message": "API Base Online! Acesse /docs para ver o Swagger."}