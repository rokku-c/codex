"""Resolve-check demo with the SQL injection fixed correctly."""

from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path("demo_users.db")


def find_user_by_name(username: str) -> list[tuple[int, str, str]]:
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = "SELECT id, username, role FROM users WHERE username = ?"
        cursor.execute(query, (username,))
        return cursor.fetchall()


if __name__ == "__main__":
    print(find_user_by_name("alice"))
