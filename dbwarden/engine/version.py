from dbwarden.constants import (
    MIGRATIONS_DIR,
)
from dbwarden.exceptions import DirectoryNotFoundError
from pathlib import Path
import re
import os
from typing import Optional


def get_migrations_directory() -> str:
    """
    Get the migrations directory path.

    Returns:
        str: Path to migrations directory.

    Raises:
        DirectoryNotFoundError: If migrations directory is not found.
    """
    current_dir = Path.cwd()
    migrations_dir = current_dir / MIGRATIONS_DIR

    if not migrations_dir.exists() or not migrations_dir.is_dir():
        raise DirectoryNotFoundError(
            f"migrations directory not found. Please run 'dbwarden init' first."
        )
    return str(migrations_dir)


MIGRATION_PATTERN = re.compile(r"^(\d{4})_(.+)\.sql$")


def get_migration_filepaths_by_version(
    directory: str,
    version_to_start_from: Optional[str] = None,
    end_version: Optional[str] = None,
) -> dict[str, str]:
    """
    Get migration file paths grouped by version.

    Args:
        directory: Path to migrations directory.
        version_to_start_from: Only get migrations after this version.
        end_version: Only get migrations up to this version.

    Returns:
        dict[str, str]: Mapping of version to file path.
    """
    migrations: dict[str, str] = {}

    if not os.path.exists(directory):
        return {}

    for filename in sorted(os.listdir(directory)):
        match = MIGRATION_PATTERN.match(filename)
        if match:
            version = match.group(1)
            filepath = os.path.join(directory, filename)
            migrations[version] = filepath

    if version_to_start_from:
        versions = list(migrations.keys())
        start_idx = (
            versions.index(version_to_start_from) + 1
            if version_to_start_from in versions
            else 0
        )
        migrations = {k: v for k, v in list(migrations.items())[start_idx:]}

    if end_version:
        versions = list(migrations.keys())
        if end_version in versions:
            end_idx = versions.index(end_version)
            migrations = {k: v for k, v in list(migrations.items())[: end_idx + 1]}

    return migrations


def get_next_migration_number(directory: str) -> str:
    """
    Get the next migration number for a new migration.

    Args:
        directory: Path to migrations directory.

    Returns:
        str: Next migration number as 4-digit string.
    """
    existing_migrations = get_migration_filepaths_by_version(directory)
    if not existing_migrations:
        return "0001"

    existing_numbers = []
    for version in existing_migrations.keys():
        if version.isdigit():
            existing_numbers.append(int(version))

    if existing_numbers:
        next_num = max(existing_numbers) + 1
    else:
        next_num = 1

    return f"{next_num:04d}"


def parse_version_string(version: str) -> tuple[int, ...]:
    """Parse a version string into a tuple of integers."""
    return tuple(int(x) for x in version.split("."))


def compare_versions(v1: str, v2: str) -> int:
    """
    Compare two version strings.

    Returns:
        -1 if v1 < v2, 0 if v1 == v2, 1 if v1 > v2
    """
    p1 = parse_version_string(v1)
    p2 = parse_version_string(v2)

    if p1 < p2:
        return -1
    elif p1 > p2:
        return 1
    return 0
