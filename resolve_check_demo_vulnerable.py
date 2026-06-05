"""Resolve-check demo with two obvious vulnerabilities."""

from __future__ import annotations

import sqlite3
import subprocess
from pathlib import Path

DB_PATH = Path("demo_users.db")


def find_user_by_name(username: str) -> list[tuple[int, str, str]]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = (
            "SELECT id, username, role FROM users "
            f"WHERE username = '{username}'"
        )
        cursor.execute(query)
        return cursor.fetchall()


def ping_host(host: str) -> str:
    return subprocess.check_output(f"ping -c 1 {host}", shell=True, text=True)


if __name__ == "__main__":
    print(find_user_by_name("alice"))
    print(ping_host("127.0.0.1"))
