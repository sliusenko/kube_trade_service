from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "../../services"))

# імпортуємо Base з усіх сервісів
from services.core_admin.app.models.base import Base
from services.core_admin.app import models as admin_models
from services.core_fetch.app import models as fetch_models
from services.core_news.app import models as news_models

target_metadata = Base.metadata

# об’єднуємо metadata
target_metadata = [
    AdminBase.metadata,
    FetchBase.metadata,
    PriceBase.metadata,
    NewsBase.metadata,
]

def run_migrations_offline():
    context.configure(
        url=os.getenv("DATABASE_URL"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine_from_config(
        context.config.get_section(context.config.config_ini_section),
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
