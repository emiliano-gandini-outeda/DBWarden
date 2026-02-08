import hashlib
from typing import List


def calculate_checksum(sql_statements: list[str]) -> str:
    """
    Calculate SHA256 checksum of SQL statements.

    Args:
        sql_statements: List of SQL statements.

    Returns:
        str: SHA256 checksum of the statements.
    """
    content = ";".join(sql_statements)
    return hashlib.sha256(content.encode()).hexdigest()
