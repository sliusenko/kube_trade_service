from logging.config import fileConfig
from alembic import context
from sqlalchemy import engine_from_config, pool
from core_fetch.db.models import Base  # 👈 імпорт твоїх моделей (Exchange, ExchangeSymbol, тощо)

# Конфіг із alembic.ini
config = context.config
fileConfig(config.config_file_name)

# Метадані з твоїх моделей
target_metadata = Base.metadata


def run_migrations_offline():
    """Запуск у офлайн-режимі (генерація SQL без виконання)."""
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Запуск у онлайн-режимі (виконання змін у БД)."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
