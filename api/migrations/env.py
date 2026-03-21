import logging
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

from src.db.session import BASE, DATABASE_URL
# Importa todos tus modelos para que Alembic los detecte
import src.models  # ajusta este import según tu estructura

config = context.config

if config.config_file_name:
    fileConfig(config.config_file_name)

logger = logging.getLogger('alembic.env')

config.set_main_option('sqlalchemy.url', DATABASE_URL)

target_metadata = BASE.metadata


def run_migrations_offline():
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    def process_revision_directives(context, revision, directives):
        if getattr(config.cmd_opts, 'autogenerate', False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info('No changes in schema detected.')

    connectable = engine_from_config(
        config.get_section(config.config_ini_section) or {},
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            process_revision_directives=process_revision_directives,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()