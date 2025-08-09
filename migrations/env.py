from alembic import context
from logging.config import fileConfig
from app.db import engine, Base

config = context.config
fileConfig(config.config_file_name)

def run_migrations_online():
    with engine.connect() as connection:
        context.configure(connection=connection, target_metadata=Base.metadata)
        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
