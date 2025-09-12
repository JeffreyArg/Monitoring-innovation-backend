# app/database/migrations/env.py
import os
from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from app.database.base import Base

try:
    from dotenv import load_dotenv
    load_dotenv(encoding="utf-8")
except Exception:
    pass

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def get_database_url() -> str:
    url = (
        os.getenv("DATABASE_URL")
        or os.getenv("DATABASE_INTERNAL_URL")
        or os.getenv("RENDER_INTERNAL_DATABASE_URL")
        or ""
    )
    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg2://", 1)
    return url

db_url = get_database_url()
if not db_url:
    raise RuntimeError("DATABASE_URL no está definido en tiempo de ejecución.")

config.set_main_option("sqlalchemy.url", db_url)

target_metadata = Base.metadata
autogen_opts = {"compare_type": True, "compare_server_default": True}

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        **autogen_opts,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata, **autogen_opts)
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
