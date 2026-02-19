from fastapi import FastAPI
from app.routers import mock_router

app = FastAPI(
    title="AgroLocal API",
    description="API do Marketplace de Agricultura Familiar",
    version="0.2.0"
)

# --- Registro de Rotas ---

# Registra o Mock Router (Disponibiliza as rotas em /mocks/...)
app.include_router(mock_router.router)

# Futuro: Aqui entraremos com app.include_router(auth_router.router) na Sprint 03
# Futuro: Aqui entraremos com app.include_router(order_router.router) na Sprint 04

@app.get("/")
def read_root():
    """Rota de Health Check."""
    return {"message": "API AgroLocal Online! Acesse /docs para ver a documentação."}