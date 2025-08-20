import os
from alembic import command
from alembic.config import Config


def run_migrations() -> None:
    """Apply database migrations."""
    cfg = Config(os.path.join(os.path.dirname(__file__), "alembic.ini"))
    command.upgrade(cfg, "head")


if __name__ == "__main__":
    run_migrations()
    print("Database migrated")
