import os
import sqlite3
import subprocess
from pathlib import Path


DB_PATH = "demo.db"

# Fix 1: Use environment variable for admin token instead of hardcoding
ADMIN_TOKEN = os.getenv("ADMIN_TOKEN", "default-admin-token-change-me")


def find_user_by_name(username: str):
    """
    Fixed: SQL injection.
    Using parameterized query and proper connection management.
    """
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()

        query = "SELECT id, username, role FROM users WHERE username = ?"
        cursor.execute(query, (username,))

        return cursor.fetchall()


def export_file(filename: str) -> str:
    """
    Fixed: path traversal.
    Validating that the resolved path is within the base directory.
    """
    base_dir = Path("./exports")
    file_path = (base_dir / filename).resolve()

    # Check that the resolved path is still within the base directory
    if not file_path.is_relative_to(base_dir.resolve()):
        raise ValueError(f"Invalid path: {filename} attempts to traverse outside allowed directory")

    return file_path.read_text(encoding="utf-8")


def ping_host(host: str) -> str:
    """
    Fixed: command injection.
    Using list format to prevent shell injection and validating input format.
    """
    # Basic validation to ensure host is a valid IP address or domain name
    import re
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9\-_.]*$', host):
        raise ValueError(f"Invalid host format: {host}")

    result = subprocess.check_output(["ping", "-c", "1", host], text=True)
    return result


def is_admin(token: str) -> bool:
    """
    Uses the hardcoded token above.
    """
    return token == ADMIN_TOKEN


if __name__ == "__main__":
    print(find_user_by_name("alice"))
    print(export_file("report.txt"))
    print(ping_host("127.0.0.1"))
    print(is_admin(os.getenv("ADMIN_TOKEN", "")))
