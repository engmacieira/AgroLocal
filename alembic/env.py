from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# 1. Importar a Configuração do Projeto
from app.core.config import settings

# 2. Importar o Base e TODOS os Models
# Se não importar aqui, o Alembic não vê as tabelas!
from app.core.database import Base
from app.models import (
    user_model,
    address_model,
    catalog_model,
    product_model,
    order_model,
    transaction_model,
    payout_model,
    review_model,
    audit_model
)

# Configuração do Alembic
config = context.config

# 3. Sobrescrever a URL do banco com a do nosso settings (Docker/Postgres)
# Isso garante que ele use a mesma conexão da aplicação (porta 5434, etc)
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Configuração de Log
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# 4. Apontar o Metadata para o Autogenerate
target_metadata = Base.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            user_module_prefix="app.core.database.",
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()