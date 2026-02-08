import json
import yaml

from dbwarden.config import get_config, get_non_secret_env_vars
from dbwarden.constants import DBWARDEN_VERSION
from dbwarden.database.connection import get_mode, is_async_enabled
from dbwarden.logging import get_logger


def mode_cmd() -> None:
    """Display current execution mode (sync or async)."""
    mode = get_mode()
    print(f"Execution mode: {mode}")
    print(f"Async enabled: {is_async_enabled()}")


def env_cmd() -> None:
    """Display relevant environment variables without leaking secrets."""
    logger = get_logger()
    config = get_config()
    env_vars = get_non_secret_env_vars()

    print("DBWarden Environment Configuration:")
    print("=" * 50)
    print(f"DBWARDEN_SQLALCHEMY_URL: {env_vars.get('DBWARDEN_SQLALCHEMY_URL', '***')}")
    print(f"DBWARDEN_ASYNC: {env_vars.get('DBWARDEN_ASYNC', 'false')}")
    print(f"DBWARDEN_MODEL_PATHS: {env_vars.get('DBWARDEN_MODEL_PATHS', '(not set)')}")
    print(
        f"DBWARDEN_POSTGRES_SCHEMA: {env_vars.get('DBWARDEN_POSTGRES_SCHEMA', '(not set)')}"
    )


def version_cmd() -> None:
    """Display DBWarden version."""
    print(DBWARDEN_VERSION)
