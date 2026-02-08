import os
import re
from typing import Optional


def get_description_from_filename(filename: str) -> str:
    """
    Extract description from migration filename.

    Args:
        filename: Migration filename (e.g., "V1__create_users_table.sql")

    Returns:
        str: Description extracted from filename.
    """
    parts = filename.split("__")
    if len(parts) >= 2:
        return parts[1].replace(".sql", "").replace("_", " ").strip()
    return filename.replace(".sql", "").replace("_", " ").strip()


def parse_upgrade_statements(file_path: str) -> list[str]:
    """
    Parse upgrade statements from a migration file.

    Args:
        file_path: Path to the migration SQL file.

    Returns:
        list[str]: List of SQL statements for upgrade.
    """
    with open(file_path, "r") as f:
        content = f.read()

    return _extract_section_statements(content, "-- upgrade")


def parse_rollback_statements(file_path: str) -> list[str]:
    """
    Parse rollback statements from a migration file.

    Args:
        file_path: Path to the migration SQL file.

    Returns:
        list[str]: List of SQL statements for rollback.
    """
    with open(file_path, "r") as f:
        content = f.read()

    return _extract_section_statements(content, "-- rollback")


def _extract_section_statements(content: str, section_marker: str) -> list[str]:
    """
    Extract SQL statements from a section of a migration file.

    Args:
        content: Full content of the migration file.
        section_marker: Marker indicating the section start (e.g., "-- upgrade").

    Returns:
        list[str]: List of SQL statements.
    """
    lines = content.split("\n")
    statements: list[str] = []
    current_statement: list[str] = []
    in_section = False

    for line in lines:
        stripped = line.strip()

        if stripped == section_marker:
            in_section = True
            continue

        if stripped == "-- rollback" and in_section:
            if current_statement:
                statement = "\n".join(current_statement).strip()
                if statement:
                    statements.append(statement)
                current_statement = []
            in_section = False
            continue

        if in_section:
            if stripped and not stripped.startswith("--"):
                current_statement.append(line)
            elif current_statement and not stripped:
                statement = "\n".join(current_statement).strip()
                if statement:
                    statements.append(statement)
                current_statement = []

    if current_statement:
        statement = "\n".join(current_statement).strip()
        if statement:
            statements.append(statement)

    return statements
